import re
from typing import List, Optional, Dict
from dataclasses import dataclass

@dataclass
class M3UChannel:
    name: str
    url: str
    group: Optional[str] = None
    logo: Optional[str] = None
    epg_id: Optional[str] = None
    extra_info: Dict[str, str] = None

class M3UParser:
    def __init__(self, content: str):
        self.content = content
        self.channels: List[M3UChannel] = []

    def parse(self) -> List[M3UChannel]:
        # Split content into lines
        lines = self.content.splitlines()
        
        current_extinf = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("#EXTINF:"):
                # Extract metadata from EXTINF line
                # Example: #EXTINF:-1 tvg-id="ChannelID" tvg-logo="logo_url" group-title="Group Name",Channel Name
                
                # Use regex to find all key="value" patterns
                metadata = {}
                matches = re.findall(r'([\w-]+)="([^"]*)"', line)
                for key, value in matches:
                    metadata[key] = value
                
                # The part after the last comma is the channel name
                parts = line.split(',', 1)
                name = parts[1] if len(parts) > 1 else "Unknown Channel"
                
                current_extinf = {
                    "name": name,
                    "metadata": metadata
                }
                
            elif line.startswith("http") and current_extinf:
                # This is the URL for the channel
                url = line
                
                group = current_extinf["metadata"].get("group-title")
                logo = current_extinf["metadata"].get("tvg-logo")
                epg_id = current_extinf["metadata"].get("tvg-id")
                
                self.channels.append(M3UChannel(
                    name=current_extinf["name"],
                    url=url,
                    group=group,
                    logo=logo,
                    epg_id=epg_id,
                    extra_info=current_extinf["metadata"]
                ))
                
                # Reset for next channel
                current_extinf = None
                
        return self.channels

# Note: The regex usage in my thought process was slightly wrong, 
# I'll rewrite the parser more robustly.
