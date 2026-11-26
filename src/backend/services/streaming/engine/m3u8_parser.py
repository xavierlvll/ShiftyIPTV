from typing import List, Optional, Dict, Set
import re

class M3U8Parser:
    """A parser for M3U8 (HLS) playlists, supporting master and media playlists."""
    def __init__(self, content: str, base_url: Optional[str] = None):
        self.content = content
        self.base_url = base_url
        self.playlists: List[str] = []
        self.segments: List[str] = []
        self.discontinuities: List[int] = []
        self.is_master = False
        self.is_parsed = False

    def _resolve_url(self, url: str) -> str:
        if not self.base_url:
            return url
        if url.startswith("http"):
            return url
        if url.startswith("/"):
            # This is a simplification. A real implementation would handle absolute paths correctly.
            return f"{self.base_url.rstrip('/')}{url}"
        return f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"

    def parse(self) -> tuple[bool, List[str], List[str], Optional[int]]:
        """Parses the playlist content and returns (is_master, playlists, segments, media_sequence_number)."""
        if self.is_parsed:
            return self.is_master, self.playlists, self.segments, getattr(self, 'media_sequence_number', None)
        
        lines = self.content.splitlines()
        media_sequence_number = None
        
        # Check if it's a master playlist
        if any("#EXT-X-STREAM-INF" in line for line in lines):
            self.is_master = True
            for line in lines:
                if line.startswith("http") or line.startswith("/"):
                    self.playlists.append(self._resolve_url(line.strip()))
        else:
            self.is_master = False
            for i, line in enumerate(lines):
                if "#EXT-X-DISCONTINUITY" in line:
                    self.discontinuities.append(i)
                if line.startswith("#EXT-X-MEDIA-SEQUENCE:"):
                    try:
                        media_sequence_number = int(line.split(":")[1].strip())
                    except (ValueError, IndexError):
                        pass
                if line.startswith("http") or line.startswith("/"):
                    self.segments.append(self._resolve_url(line.strip()))
            self.media_sequence_number = media_sequence_number
        
        self.is_parsed = True
        return self.is_master, self.playlists, self.segments, media_sequence_number

        lines = self.content.splitlines()
        
        # Check if it's a master playlist
        if any("#EXT-X-STREAM-INF" in line for line in lines):
            self.is_master = True
            for line in lines:
                if line.startswith("http") or line.startswith("/"):
                    self.playlists.append(self._resolve_url(line.strip()))
        else:
            self.is_master = False
            for i, line in enumerate(lines):
                if "#EXT-X-DISCONTINUITY" in line:
                    self.discontinuities.append(i)
                if line.startswith("http") or line.startswith("/"):
                    self.segments.append(self._resolve_url(line.strip()))
        
        self.is_parsed = True
        return self.is_master, self.playlists, self.segments
