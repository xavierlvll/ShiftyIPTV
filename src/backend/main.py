from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.db.session import get_db, init_db
from src.backend.api.providers import router as provider_router
from src.backend.api.channels import router as channel_router

app = FastAPI(title="SHiFTyIPTV")

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(provider_router, prefix="/api/providers", tags=["providers"])
app.include_router(channel_router, prefix="/api/channels", tags=["channels"])

@app.get("/")
async def root():
    return {"message": "SHiFTyIPTV API is running"}
