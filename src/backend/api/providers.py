from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from src.backend.db.session import get_db
from src.backend.models.models import Provider, Channel
from src.backend.schemas.schemas import Provider, ProviderCreate

router = APIRouter()

@router.post("/", response_model=Provider)
async def create_provider(provider_in: ProviderCreate, db: AsyncSession = Depends(get_db)):
    new_provider = Provider(**provider_in.dict())
    db.add(new_provider)
    await db.commit()
    await db.refresh(new_provider)
    return new_provider

@router.get("/", response_model=List[Provider])
async def read_providers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Provider))
    providers = result.scalars().all()
    return providers

@router.get("/{provider_id}", response_model=Provider)
async def read_provider(provider_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Provider).where(Provider.id == provider_id))
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@router.delete("/{provider_id}", response_model=bool)
async def delete_provider(provider_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Provider).where(Provider.id == provider_id))
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    await db.delete(provider)
    await db.commit()
    return True
