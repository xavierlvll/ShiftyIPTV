from typing import List, Optional, Dict
import datetime
import json
from dataclasses import dataclass, asdict

@dataclass
class StreamEvent:
    """Represents a monitoring event for a specific stream."""
    timestamp: str
    event_type: str  # e.g., 'segment_failure', 'playlist_update', 'reconnection', 'error'
    description: str
    channel_id: int

class StreamMonitor:
    """Manimates stream events and provides history for monitoring."""
    def __init__(self):
        self.events: List[dict] = []

    def log_event(self, channel_id: int, event_type: str, description: str):
        """Logs a new event with the current timestamp."""
        event = StreamEvent(
            timestamp=datetime.datetime.now().isoformat(),
            event_type=event_type,
            description=description,
            channel_id=channel_id
        )
        self.events.append(asdict(event))

    def get_history(self, channel_id: Optional[int] = None) -> List[dict]:
        """Retrietyves event history, optionally filtered by channel_id."""
        if channel_id is not None:
            return [e for e in self.events if e['channel_id'] == channel_id]
        return self.events

    def clear_history(self, channel_id: Optional[int] = None):
        """Clears event history, optionally for a specific channel."""
        if channel_id is not None:
            self.events = [e for e in self.events if e['channel_id'] != channel_id]
        else:
            self.events = []
