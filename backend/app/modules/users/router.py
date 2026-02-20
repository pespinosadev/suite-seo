from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, require_role
from app.modules.users import schemas, service

router = APIRouter()


@router.get("/", response_model=list[schemas.UserListItem])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role("admin")),
):
    return await service.list_users(db)


@router.get("/roles", response_model=list[schemas.RoleOut])
async def list_roles(
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role("admin")),
):
    return await service.list_roles(db)


@router.post("/", response_model=schemas.UserListItem, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_role("admin")),
):
    return await service.create_user(body, db)


@router.put("/{user_id}", response_model=schemas.UserListItem)
async def update_user(
    user_id: int,
    body: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    return await service.update_user(user_id, body, current_user.id, db)


@router.put("/me/profile", response_model=schemas.UserListItem)
async def update_my_profile(
    body: schemas.UpdateProfileRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await service.update_my_profile(current_user.id, body, db)


@router.put("/me/smtp-password", response_model=schemas.UserListItem)
async def set_my_smtp_password(
    body: schemas.SetSmtpPasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await service.set_smtp_password(current_user.id, body, db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role("admin")),
):
    await service.delete_user(user_id, current_user.id, db)
