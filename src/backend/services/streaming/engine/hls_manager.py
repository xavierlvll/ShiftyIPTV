from src.backend.services.streaming.engine.m3u8_parser import M3U8Parser
from src.backend.services.streaming.engine.segment_tracker import SegmentTracker
import httpx
import asyncio
import logging
from typing import Optional, List, Dict
from src.backend.services.streaming.engine.core import StreamSession
from src.backend.services.streaming.engine.monitor import StreamMonitor

logger = logging.getLogger(__name__)

class HLSManager:
    """Manages the HLS playlist and segments for a stream session."""
    def __init__(self, session: StreamSession, monitor: StreamMonitor):
        self.session = session
        self.monitor = monitor
        self.tracker = SegmentTracker(session.channel_id)
        self.master_playlist_url: Optional[str] = None
        self.media_playlist_url: Optional[str] = None
        self._is_running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self, initial_url: str):
        """Starts the HLS management loop."""
        self.media_playlist_url = initial_url
        self.session.stream_url = initial_url
        self._is_running = True
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        """Stops the HLS management loop."""
        self._is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run_loop(self):
        """The main loop that periodically checks for playlist updates."""
        while self._is_running:
            try:
                await self._refresh_playlist()
                # Reset failure count on successful refresh
                self.session.failure_count = 0
            except Exception as e:
                self.session.failure_count += 1
                self.monitor.log_event(
                    self.session.channel_id, 
                    "playlist_error", 
                    f"Error refreshing playlist (failure #{self.session.failure_count}): {str(e)}"
                )
            
            # Exponential backoff: 10s, 20s, 40s, 80s, up to 300s (5 mins)
            delay = min(10 * (2 ** (self.session.failure_count - 1) if self.session.failure_count > 0 else 0), 300)
            if self.session.failure_count > 0:
                self.monitor.log_event(
                    self.session.channel_id,
                    "retry_scheduled",
                    f"Retrying in {delay} seconds due to failure"
                )
            
            await asyncio.sleep(delay)

    async def _refresh_playlist(self):
        """Fetches and parses the current playlist to detect changes."""
        if not self.media_playlist_url:
            return

        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            try:
                response = await client.get(self.media_playlist_url)
                if str(response.url) != self.media_playlist_url:
                    self.media_playlist_url = str(response.url)
                    self.monitor.log_event(
                        self.session.channel_id,
                        "playlist_update",
                        f"Playlist URL redirected to: {self.media_playlist_url}"
                    )
                if response.status_code != 200:
                    self.monitor.log_event(
                        self.session.channel_id, 
                        "playlist_error", 
                        f"Upstream returned {response.status_code}"
                    )
                    return

                content = response.text
                parser = M3U8Parser(content, base_url=self.media_playlist_url)
                is_master, playlists, segments, media_sequence_number = parser.parse()
                
                if is_master:
                    if playlists and (not self.media_playlist_url or playlists[0] != self.media_playlist_url):
                        self.media_playlist_url = playlists[0]
                        self.session.stream_url = playlists[0]

                        self.monitor.log_event(
                            self.session.channel_id,
                            "playlist_update",
                            f"Switched to new media playlist: {self.media_playlist_url}"
                        )
                else:
                    if segments and (not self.media_playlist_url or segments[0] != self.media_playlist_url):
                        self.session.stream_url = segments[0]

                        self.media_playlist_url = segments[0]
                        self.monitor.log_event(
                            self.session.channel_id,
                            "playlist_update",
                            f"Switched to new media playlist: {self.media_playlist_url}"
                        )
                    
                    # Track segments for anomalies
                    for segment_url in segments:
                        anomalies = self.tracker.track_segment(segment_url)
                        for anomaly in anomalies:
                            self.monitor.log_event(
                                self.session.channel_id,
                                "segment_anomaly",
                                anomaly
                            )
                    
                    # Check for discontinuities in the media playlist
                    if parser.discontinuities:
                        self.monitor.log_event(
                            self.session.channel_id,
                            "discontinuity_detected",
                            f"Detected {len(parser.discontinuities)} discontinuity markers"
                        )

                    if media_sequence_number is not None:
                        self.tracker.update_sequence_number(media_sequence_number)
                
                self.monitor.log_event(
                    self.session.channel_id,
                    "playlist_update",
                    "Playlist refreshed successfully"
                )
            except Exception as e:
                self.monitor.log_event(
                    self.session.channel_id,
                    "playlist_error",
                    f"Failed to fetch playlist: {str(e)}"
                )
                raise

    def attend_channel_id(self) -> int:
        return self.session.channel_id

