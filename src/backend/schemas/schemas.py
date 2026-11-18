from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ProviderBase(BaseModel):
    name: str
    url: HttpUrl
    type: Optional[str] = "m3u"
    enabled: bool = True

class ProviderCreate(ProviderBase):
    pass

class Provider(ProviderBase):
    id: int
    last_refresh: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChannelBase(BaseModel):
    name: str
    group: Optional[str] = None
    logo: Optional[HttpUrl] = None
    epg_id: Optional[str] = None
    stream_url: HttpUrl
    enabled: bool = True

class ChannelCreate(ChannelBase):
    provider_id: int

class Channel(ChannelBase):
    id: int
    provider_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
