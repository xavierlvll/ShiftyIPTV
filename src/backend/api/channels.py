from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from src.backend.db.session import get_db
from src.backend.models.models import Provider, Channel
from src.backend.schemas.schemas import Channel, ChannelCreate
from src.backend.services.channel_service import ChannelService

router = APIRouter()

@router.post("/", response_model=Channel)
async def create_channel(channel_in: ChannelCreate, db: AsyncSession = Depends(get_db)):
    new_channel = Channel(**channel_in.dict())
    db.add(new_channel)
    await db.commit()
    await db.refresh(new_channel)
    return new_channel

@router.get("/", response_model=List[Channel])
async def read_channels(provider_id: int = None, db: AsyncSession = Depends(get_db)):
    service = ChannelService(db)
    return await service.get_all_channels(provider_id=provider_id if provider_id else None)

@router.get("/{channel_id}", response_model=Channel)
async def read_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    service = ChannelService(db)
    channel = await service.get_channel(channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@router.patch("/{channel_id}", response_model=Channel)
async def update_channel(channel_id: int, channel_update: dict, db: AsyncSession = Depends(get_db)):
    service = ChannelService(db)
    updated_channel = await service.update_channel(channel_id, channel_update)
    if not updated_channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return updated_channel

@router.delete("/{channel_id}", response_model=bool)
async def delete_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    service = ChannelService(db)
    return await service.delete_channel(channel_id)
