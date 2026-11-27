from fastapi import Request, Response, HTTPException
import httpx
import asyncio
from src.backend.services.streaming.engine.core import StreamingEngine, StreamSession
from src.backend.models.models import Channel
from src.backend.services.channel_service import ChannelService
from src.backend.db.session import AsyncSession

class StreamDeliveryService:
    def __init__(self, db: AsyncSession, engine: StreamingEngine):
        self.db = db
        self.engine = engine


    async def get_stream_response(self, channel_id: int, request: Request) -> Response:
        """
        Handles the incoming HTTP request for a stream and streams the content from the upstream.
        """
        channel_service = ChannelService(self.db)
        channel = await channel_service.get_channel(channel_id)
        
        if not channel or not channel.is_enabled:
            raise HTTPException(status_code=404, detail="Channel not found or disabled")

        session = await self.engine.get_or_create_for_channel(channel_id, channel_service)
        if not session:
            raise HTTPException(status_code=500, detail="Failed to create stream session")
        
        async def stream_generator():
            async with httpx.AsyncClient(timeout=None) as client:
                try:
                    async with client.stream("GET", session.stream_url) as response:
                        if response.status_code != 200:
                            yield f"Error: Upstream returned {response.status_code}".encode()
                            return

                        async for chunk in response.aiter_bytes():
                            yield chunk
                except Exception as e:
                    session.error_log.append(f"Connection error: {str(e)}")
                    yield b"Stream connection error"
                                
        return Response(content=stream_generator(), media_type="application/octet-stream")

