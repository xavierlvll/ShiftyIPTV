import httpx
from typing import List, Optional, Dict

class M3U8Parser:
    """A simple parser for M3U8 (HLS) playlists."""
    def __init__(self, content: str):
        self.content = content
        self.playlists: List[str] = []
        self.segments: List[str] = []
        self.is_master = False

    def parse(self):
        lines = self.content.splitlines()
        
        # Check if it's a master playlist
        if any("#EXT-X-STREAM-INF" in line for line in lines):
            self.is_master = True
            for line in lines:
                if line.startswith("http") or line.startswith("/"):
                    # For simplicity, we assume absolute URLs
                    self.playlists.append(line.strip())
        else:
            self.is_master = False
            for i, line in enumerate(lines):
                if "#EXT-X-DISCONTINUITY" in line:
                    self.discontinuities.append(i)
                if line.startswith("http") or line.startswith("/"):
                    self.segments.append(line.strip())
        
        return self.is_master, self.playlists, self.segments

