from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from src.backend.db.session import get_db
from src.backend.models.models import Provider, Channel
from src.backend.schemas.schemas import Channel, ChannelCreate

router = APIRouter()

@router.post("/", response_model=Channel)
async def create_channel(channel_in: ChannelCreate, db: AsyncSession = Depends(get_db)):
    new_channel = Channel(**channel_in.dict())
    db.add(new_channel)
    await db.commit()
    await db.refresh(new_channel)
    return new_channel

@router.get("/", response_model=List[Channel])
async def read_channels(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Channel).options(selectinload(Channel.provider)))
    channels = result.scalars().all()
    return channels

@router.get("/{channel_id}", response_model=Channel)
async def read_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Channel).where(Channel.id == channel_id).options(selectinload(Channel.provider)))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@router.delete("/{channel_id}", response_model=bool)
async def delete_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    await db.delete(channel)
    await db.commit()
    return True
