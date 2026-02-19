import asyncio
import argparse
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.modules.auth.models import User, Role


async def create_user(email: str, password: str, role_name: str) -> None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Role).where(Role.name == role_name))
        role = result.scalar_one_or_none()
        if not role:
            print(f"Error: role '{role_name}' not found. Arranca la app primero para crear los roles.")
            return

        result = await db.execute(select(User).where(User.email == email))
        if result.scalar_one_or_none():
            print(f"Error: el usuario '{email}' ya existe.")
            return

        db.add(User(email=email, hashed_password=hash_password(password), role_id=role.id))
        await db.commit()
        print(f"Usuario '{email}' creado con rol '{role_name}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--role", choices=["admin", "responsable", "usuario"], required=True)
    args = parser.parse_args()
    asyncio.run(create_user(args.email, args.password, args.role))
