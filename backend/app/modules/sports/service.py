from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.sports.models import SportEvent
from app.modules.sports.schemas import SportEventIn


async def replace_events(events: list[SportEventIn], db: AsyncSession) -> list[SportEvent]:
    await db.execute(delete(SportEvent))
    for e in events:
        db.add(SportEvent(
            day_name=e.dia,
            event_date=e.fecha,
            deporte=e.deporte,
            hora=e.hora,
            competicion=e.competicion,
            evento=e.evento,
            canal=e.canal,
        ))
    await db.commit()
    result = await db.execute(select(SportEvent).order_by(SportEvent.hora))
    return result.scalars().all()


async def list_events(db: AsyncSession) -> list[SportEvent]:
    result = await db.execute(select(SportEvent).order_by(SportEvent.hora))
    return result.scalars().all()
