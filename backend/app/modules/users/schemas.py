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
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
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


class SetSmtpPasswordRequest(BaseModel):
    smtp_password: str


class UpdateProfileRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    smtp_password: Optional[str] = None
    clear_smtp_password: bool = False
