from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.backend.models.models import Provider, Channel
from src.backend.services.m3u.parser import M3UParser
import httpx
from datetime import datetime

class ProviderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_from_m3u(self, name: str, url: str) -> Provider:
        # First, fetch the M3U content
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch M3U: {response.status_code}")
            content = response.text

        # Parse the content
        parser = M3UParser(content)
        channels_data = parser.parse()

        # Create the provider
        new_provider = Provider(name=name, url=url, type="m3u")
        self.db.add(new_provider)
        await self.db.flush()  # Get the provider ID

        # Create channels
        new_channels = []
        for ch in channels_data:
            channel = Channel(
                provider_id=new_provider.id,
                name=ch.name,
                group=ch.group,
                logo=ch.logo,
                epg_id=ch.epg_id,
                stream_url=ch.url,
                extra_info=ch.extra_info if ch.extra_info else {}
            )
            new_channels.append(channel)
        
        self.db.add_all(new_channels)
        await self.db.commit()
        await self.db.refresh(new_provider)
        
        return new_provider

    async def refresh_provider(self, provider_id: int) -> int:
        # Fetch the provider
        result = await self.db.execute(select(Provider).where(Provider.id == provider_id))
        provider = result.scalar_one_or_none()
        if not provider:
            raise Exception("Provider not found")

        # Fetch the M3U content
        async with httpx.AsyncClient() as client:
            response = await client.get(provider.url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch M3U: {response.status_code}")
            content = response.text

        # Parse the content
        parser = M3UParser(content)
        channels_data = parser.parse()

        # Clear existing channels for this provider
        from sqlalchemy import delete
        await self.db.execute(delete(Channel).where(Channel.provider_id == provider_id))

        # Create new channels
        new_channels = []
        for ch in channels_data:
            channel = Channel(
                provider_id=provider.id,
                name=ch.name,
                group=ch.group,
                logo=ch.logo,
                epg_id=ch.epg_id,
                stream_url=ch.str_url if hasattr(ch, 'str_url') else ch.url,
                extra_info=ch.extra_info if ch.extra_info else {}
            )
            new_channels.append(channel)
        
        self.db.add_all(new_channels)
        provider.last_refresh = datetime.now()
        await self.db.commit()
        
        return len(new_channels)
