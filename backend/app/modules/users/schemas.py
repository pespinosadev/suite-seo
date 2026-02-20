import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class RoleOut(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class UserListItem(BaseModel):
    id: int
    email: str
    is_active: bool
    role: RoleOut
    created_at: datetime.datetime
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role_id: int
    is_active: bool = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None
