from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_role
from app.modules.domains import schemas, service

router = APIRouter()


# ── Categories ──────────────────────────────────────────────

@router.get("/categories", response_model=list[schemas.CategoryOut])
async def list_categories(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.list_categories(db)


@router.post("/categories", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(
    body: schemas.CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role("admin")),
):
    return await service.create_category(body, db)


@router.put("/categories/{cat_id}", response_model=schemas.CategoryOut)
async def update_category(
    cat_id: int,
    body: schemas.CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role("admin")),
):
    return await service.update_category(cat_id, body, db)


@router.delete("/categories/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    cat_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role("admin")),
):
    await service.delete_category(cat_id, db)


# ── Domains ─────────────────────────────────────────────────

@router.get("/", response_model=list[schemas.DomainOut])
async def list_domains(
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    return await service.list_domains(db)


@router.post("/", response_model=schemas.DomainOut, status_code=status.HTTP_201_CREATED)
async def create_domain(
    body: schemas.DomainCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role("admin")),
):
    return await service.create_domain(body, db)


@router.put("/{dom_id}", response_model=schemas.DomainOut)
async def update_domain(
    dom_id: int,
    body: schemas.DomainUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role("admin")),
):
    return await service.update_domain(dom_id, body, db)


@router.delete("/{dom_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_domain(
    dom_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role("admin")),
):
    await service.delete_domain(dom_id, db)
