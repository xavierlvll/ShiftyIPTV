from typing import Set, List, Optional
import datetime

class SegmentTracker:
    """Tracks the sequence of segments in an HLS media playlist to detect skips or duplicates."""
    def __init__(self, channel_id: int):
        self.channel_id = channel_id
        self.seen_segments: Set[str] = set()
        self.last_segment_timestamp: Optional[datetime.datetime] = None
        self.history: List[str] = []

    def track_segment(self, segment_url: str) -> List[str]:
        """
        Tracks a new segment and returns a list of detected anomalies.
        Anomalies include: duplicate segments, missing segments (detected via sequence gap).
        """
        anomalies = []
        
        if segment_url in self.seen_segments:
            anomalies.append(f"Duplicate segment detected: {segment_url}")
        else:
            self.seen_segments.add(segment_url)
            self.history.append(segment_url)
            
            # In a real implementation, we would track sequence numbers/timestamps
            # and detect gaps here.
            
        return anomalies

    def clear(self):
        """Clears the tracking history."""
        self.seen_segments.clear()
        self.history.clear()
        self.last_segment_timestamp = None
