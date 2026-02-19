from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.auth.models import Role

ROLES = ["admin", "responsable", "usuario"]


async def seed_roles(db: AsyncSession) -> None:
    for name in ROLES:
        result = await db.execute(select(Role).where(Role.name == name))
        if not result.scalar_one_or_none():
            db.add(Role(name=name))
    await db.commit()
