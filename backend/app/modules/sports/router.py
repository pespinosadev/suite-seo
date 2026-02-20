from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user
from app.core.config import settings
from app.modules.sports import schemas, service

router = APIRouter()


@router.post("/events/batch", response_model=list[schemas.SportEventOut], status_code=status.HTTP_201_CREATED)
async def batch_replace_events(
    body: list[schemas.SportEventIn],
    db: AsyncSession = Depends(get_db),
    api_key: str = Header(None, alias="X-Api-Key"),
):
    if not settings.SPORTS_API_KEY or api_key != settings.SPORTS_API_KEY:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid API key")
    return await service.replace_events(body, db)


@router.get("/events", response_model=list[schemas.SportEventOut])
async def list_events(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.list_events(db)
