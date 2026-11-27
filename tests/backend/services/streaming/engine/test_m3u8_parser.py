import pytest
from src.backend.services.streaming.engine.m3u8_parser import M3U8Parser

def test_parse_master_playlist():
    content = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=1280000,RESOLUTION=1920x1080
https://example.com/master/1rev/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=640000,RESOLUTION=1280x720
https://example.com/master/720p/index.m3u8
"""
    parser = M3U8Parser(content)
    is_master, playlists, segments, media_sequence_number = parser.parse()
    
    assert is_master is True
    assert len(playlists) == 2
    assert playlists[0] == "https://example.com/master/1rev/index.m3u8"
    assert len(segments) == 0

def test_parse_media_playlist():
    content = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXT-X-MEDIA-SEQUENCE:5
#EXTINF:10.0,
https://example.com/media/seg1.ts
#EXTINF:10.0,
https://example/media/seg2.ts
#EXT-X-ENDLIST
"""
    parser = M3U8Parser(content)
    is_master, playlists, segments, media_sequence_number = parser.parse()
    
    assert is_master is False
    assert len(playlists) == 0
    assert len(segments) == 2
    assert segments[0] == "https://example.com/media/seg1.ts"
    assert media_sequence_number == 5

def test_parse_discontinuity():
    content = """#EXTM3U
#EXTM3U
#EXTINF:10.0,
https://example.com/media/seg1.ts
#EXT-X-DISCONTINUITY
#EXTINF:10.0,
https://example.com/media/seg2.ts
"""
    parser = M3U8Parser(content)
    is_master, _, _, _ = parser.parse()
    
    assert len(parser.discontinuities) == 1
