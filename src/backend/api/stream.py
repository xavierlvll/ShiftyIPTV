from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.db.session import get_db
from src.backend.services.streaming.delivery import StreamDeliveryService
from src.backend.services.streaming.engine.core import StreamingEngine
from src.backend.services.channel_service import ChannelService
from src.backend.models.models import Channel
import httpx
from typing import Optional

router = APIRouter()

# In a real application, the engine would be managed via dependency injection (e.g., a singleton or lifecycle event)
# For now, we'll assume a global engine instance or a way to access it.
# This is a placeholder for the actual engine retrieval logic.
_engine_instance: Optional[StreamingEngine] = None

async def get_engine(request: Request) -> StreamingEngine:
    global _engineintance
    if _engine_instance is None:
        # In production, this would be initialized properly during app startup
        if hasattr(request.app.state, 'streaming_engine'):
            _engine_instance = request.app.state.streaming_engine
        else:
            # Fallback for testing/development if not properly attached to app state
            raise HTTPException(status_code=500, detail="Streaming engine not initialized in app state")
    return _engine_instance

@router.get("/stream/{channel_id}")
async def stream_channel(
    channel_id: int, 
    request: Request, 
    db: AsyncSession = Depends(get_db),
    engine: StreamingEngine = Depends(get_engine)
) -> StreamingResponse:
    """
    Exposes the stream for a given channel.
    """
    delivery_service = StreamDeliveryService(db, engine)
    
    # We need to return a StreamingResponse to maintain the streaming nature.
    # The StreamDeliveryService.get_stream_response currently returns a standard Response.
    # We will wrap the generator logic here.
    
    async def stream_generator():
        channel_service = ChannelService(db)
        channel = await channel_service.get_channel(channel_id)
        if not channel or not channel.is_enabled:
            yield b"Error: Channel not found or disabled"
            return

        async with httpx.AsyncClient(timeout=None) as client:
            try:
                async with client.stream("GET", channel.stream_url) as upstream_response:
                    if upstream_response.status_code != 200:
                        yield f"Error: Upstream returned {upstream_response.status_code}".encode()
                        return

                    async for chunk in upstream_response.aiter_bytes():
                        yield chunk
            except Exception as e:
                yield f"stream_connection_failed: {str(e)}".encode()
                return

    return StreamingResponse(stream_generator(), media_type="application/octet-stream")
