from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from src.backend.models.models import Channel, Provider
from typing import List, Optional

class ChannelService:
    def __current_id(self, db: AsyncSession, channel_id: int) -> Channel:
        pass # Placeholder

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_channel(self, channel_id: int) -> Optional[Channel]:
        result = await self.db.execute(select(Channel).where(Channel.id == channel_id))
        return result.scalar_one_or_none()

    async def get_all_channels(self, provider_id: Optional[int] = None) -> List[Channel]:
        query = select(Channel)
        if provider_id:
            query = query.where(Channel.provider_id == provider_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_channel(self, channel_id: int, channel_data: dict) -> Optional[Channel]:
        result = await self.db.execute(select(Channel).where(Channel.id == channel_id))
        channel = result.scalar_one_or_none()
        if not channel:
            return None
        
        for key, value in channel_data.items():
            if hasattr(channel, key):
                setattr(channel, key, value)
        
        await self.db.commit()
        await self.db.refresh(channel)
        return channel

    async def toggle_channel_status(self, channel_id: int, enabled: bool) -> bool:
        result = await self.db.execute(select(Channel).where(Channel.id == channel_id))
        channel = result.scalar_one_or_none()
        if not channel:
            return False
        
        channel.is_enabled = enabled
        await self.db.commit()
        return True

    async def delete_channel(self, channel_id: int) -> bool:
        result = await self.db.execute(select(Channel).where(Channel.id == channel_id))
        channel = result.scalar_one_or_none()
        if not channel:
            return False
        
        await self.db.delete(channel)
        await self.db.commit()
        return True
