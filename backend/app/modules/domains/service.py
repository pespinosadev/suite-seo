from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.domains.models import Category, Domain
from app.modules.domains.schemas import CategoryCreate, DomainCreate, DomainUpdate


# ── Categories ──────────────────────────────────────────────

async def list_categories(db: AsyncSession) -> list[Category]:
    result = await db.execute(select(Category).order_by(Category.name))
    return result.scalars().all()


async def create_category(data: CategoryCreate, db: AsyncSession) -> Category:
    existing = await db.execute(select(Category).where(Category.name == data.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Categoría ya existe")
    cat = Category(name=data.name)
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


async def update_category(cat_id: int, data: CategoryCreate, db: AsyncSession) -> Category:
    result = await db.execute(select(Category).where(Category.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    dup = await db.execute(select(Category).where(Category.name == data.name, Category.id != cat_id))
    if dup.scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Nombre ya en uso")
    cat.name = data.name
    await db.commit()
    await db.refresh(cat)
    return cat


async def delete_category(cat_id: int, db: AsyncSession) -> None:
    result = await db.execute(select(Category).where(Category.id == cat_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    has_domains = await db.execute(select(Domain).where(Domain.category_id == cat_id))
    if has_domains.scalar_one_or_none():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="La categoría tiene dominios asociados")
    await db.delete(cat)
    await db.commit()


# ── Domains ─────────────────────────────────────────────────

async def list_domains(db: AsyncSession) -> list[Domain]:
    result = await db.execute(
        select(Domain).options(selectinload(Domain.category)).order_by(Domain.name)
    )
    return result.scalars().all()


async def create_domain(data: DomainCreate, db: AsyncSession) -> Domain:
    cat = await db.execute(select(Category).where(Category.id == data.category_id))
    if not cat.scalar_one_or_none():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    dom = Domain(
        name=data.name,
        full_url=data.full_url,
        domain=data.domain,
        category_id=data.category_id,
    )
    db.add(dom)
    await db.commit()
    result = await db.execute(
        select(Domain).where(Domain.id == dom.id).options(selectinload(Domain.category))
    )
    return result.scalar_one()


async def update_domain(dom_id: int, data: DomainUpdate, db: AsyncSession) -> Domain:
    result = await db.execute(
        select(Domain).where(Domain.id == dom_id).options(selectinload(Domain.category))
    )
    dom = result.scalar_one_or_none()
    if not dom:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Dominio no encontrado")

    if data.name is not None:
        dom.name = data.name
    if data.full_url is not None:
        dom.full_url = data.full_url
    if data.domain is not None:
        dom.domain = data.domain
    if data.category_id is not None:
        cat = await db.execute(select(Category).where(Category.id == data.category_id))
        if not cat.scalar_one_or_none():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
        dom.category_id = data.category_id

    await db.commit()
    result = await db.execute(
        select(Domain).where(Domain.id == dom_id).options(selectinload(Domain.category))
    )
    return result.scalar_one()


async def delete_domain(dom_id: int, db: AsyncSession) -> None:
    result = await db.execute(select(Domain).where(Domain.id == dom_id))
    dom = result.scalar_one_or_none()
    if not dom:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Dominio no encontrado")
    await db.delete(dom)
    await db.commit()
