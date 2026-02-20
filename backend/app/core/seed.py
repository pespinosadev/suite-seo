from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.auth.models import Role
from app.modules.domains.models import Category

ROLES = ["admin", "responsable", "usuario"]
CATEGORIES = ["nacionales", "regionales", "deportivos", "verticales", "revistas"]


async def seed_roles(db: AsyncSession) -> None:
    for name in ROLES:
        result = await db.execute(select(Role).where(Role.name == name))
        if not result.scalar_one_or_none():
            db.add(Role(name=name))

    for name in CATEGORIES:
        result = await db.execute(select(Category).where(Category.name == name))
        if not result.scalar_one_or_none():
            db.add(Category(name=name))

    await db.commit()
