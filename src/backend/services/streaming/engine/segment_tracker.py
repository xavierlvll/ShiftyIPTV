from typing import Set, List, Optional
import datetime

class SegmentTracker:
    """Tracks the sequence of segments in an HLS media playlist to detect skips or duplicates."""
    def __init__(self, channel_id: int):
        self.channel_id = channel_id
        self.seen_segments: Set[str] = set()
        self.last_segment_timestamp: Optional[datetime.datetime] = None
        self.history: List[str] = []
        self.sequence_numbers: List[int] = []

    def track_segment(self, segment_url: str, sequence_number: Optional[int] = None) -> List[str]:
        """
        Tracks a new segment and returns a list of detected anomalies.
        Anomalies include: duplicate segments, missing segments (detected via sequence gap).
        """
        anomalies = []
        
        if segment_url in self.seen_segments:
            an_msg = f"Duplicate segment detected: {segment_url}"
            anomalies.append(an_msg)
        else:
            self.seen_segments.add(segment_url)
            self.history.append(segment_url)
            
            if sequence_number is not None:
                if self.sequence_numbers and sequence_number != self.sequence_numbers[-1] + 1:
                    gap = sequence_number - self.sequence_numbers[-1] - 1
                    if gap > 0:
                        anomalies.append(f"Gap detected: {gap} segments missing between {self.sequence_numbers[-1]} and {sequence_number}")
                self.sequence_numbers.append(sequence_number)
            
        return anomalies

    def clear(self):
        """Clears the tracking history."""
        self.seen_segments.clear()
        self.history.clear()
        self.sequence_numbers.clear()
        self.last_segment_timestamp = None
