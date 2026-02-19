import datetime
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RoleOut(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool
    role: RoleOut
    created_at: datetime.datetime
    model_config = {"from_attributes": True}
