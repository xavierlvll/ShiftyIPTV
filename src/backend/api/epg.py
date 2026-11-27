from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.db.session import get_db
from src/backend.services.epg.epg_service import EPGService
from pydantic import BaseModel, HttpUrl

router = APIRouter()

class EPGImportRequest(BaseModel):
    url: HttpUrl

@router.post("/import")
async def import_epg(request: EPGImportRequest, db: AsyncSession = Depends(get_db)):
    """
    Triggers an XMLTV EPG import from a given URL.
    """
    epg_service = EPGService(db)
    try:
        channels_updated = await epg_service.import_xmltv(str(request.url))
        return {"message": "EPG import successful", "channels_updated": channels_updated}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
async def get_epg_status(db: AsyncSession = Depends(get_db)):
    """
    Retrieves the current status of the EPG management system.
    """
    # Placeholder for EPG status logic
    return {"status": "operational", "last_import": None}
