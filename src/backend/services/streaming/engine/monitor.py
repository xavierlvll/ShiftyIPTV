from typing import List, Optional
from dataclasses import dataclass
import datetime

@dataclass
class StreamEvent:
    timestamp: datetime.datetime
    event_type: str  # e.g., 'segment_failure', 'playlist_update', 'reconnection'
    description: str
    channel_id: int

class StreamMonitor:
    def __init__(self):
        self.events: List[StreamEvent] = []

    def log_event(self, channel_id: int, event_type: str, description: 	str):
        event = StreamEvent(
            timestamp=datetime.datetime.now(),
            event_type=event_type,
            description=description,
            channel_id=channel_id
        )
        self.events.append(event)

    def get_history(self, channel_id: Optional[int] = None) -> List[StreamEvent]:
        if channel_id:
            return [e for e in self.events if e.channel_id == channel_id]
        return self.events

    def clear_history(self, channel_id: Optional[int] = None):
        if channel_id:
            self.events = [e for e in self.events if e.channel_id != channel_id]
        else:
            self.events = []
