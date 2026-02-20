from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.auth.models import User, Role
from app.core.security import hash_password
from app.modules.users.schemas import UserCreate, UserUpdate, SetSmtpPasswordRequest


async def list_users(db: AsyncSession) -> list[User]:
    result = await db.execute(
        select(User).options(selectinload(User.role)).order_by(User.id)
    )
    return result.scalars().all()


async def list_roles(db: AsyncSession) -> list[Role]:
    result = await db.execute(select(Role).order_by(Role.id))
    return result.scalars().all()


async def create_user(data: UserCreate, db: AsyncSession) -> User:
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Email ya registrado")

    role = await db.execute(select(Role).where(Role.id == data.role_id))
    if not role.scalar_one_or_none():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role_id=data.role_id,
        is_active=data.is_active,
    )
    db.add(user)
    await db.commit()

    result = await db.execute(
        select(User).where(User.email == data.email).options(selectinload(User.role))
    )
    return result.scalar_one()


async def update_user(user_id: int, data: UserUpdate, current_user_id: int, db: AsyncSession) -> User:
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.role))
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    if data.email is not None:
        dup = await db.execute(select(User).where(User.email == data.email, User.id != user_id))
        if dup.scalar_one_or_none():
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Email ya en uso")
        user.email = data.email

    if data.password is not None and data.password != "":
        user.hashed_password = hash_password(data.password)

    if data.role_id is not None:
        if user_id == current_user_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No puedes cambiar tu propio rol")
        role = await db.execute(select(Role).where(Role.id == data.role_id))
        if not role.scalar_one_or_none():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        user.role_id = data.role_id

    if data.is_active is not None:
        if user_id == current_user_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No puedes desactivarte a ti mismo")
        user.is_active = data.is_active

    await db.commit()

    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.role))
    )
    return result.scalar_one()


async def set_smtp_password(user_id: int, data: SetSmtpPasswordRequest, db: AsyncSession) -> User:
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.role))
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    user.smtp_password = data.smtp_password
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user_id: int, current_user_id: int, db: AsyncSession) -> None:
    if user_id == current_user_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No puedes eliminar tu propia cuenta")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    await db.delete(user)
    await db.commit()
