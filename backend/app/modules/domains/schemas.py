import datetime
from typing import Optional
from pydantic import BaseModel


class CategoryOut(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class CategoryCreate(BaseModel):
    name: str


class DomainOut(BaseModel):
    id: int
    name: str
    full_url: str
    domain: str
    category: CategoryOut
    created_at: datetime.datetime
    model_config = {"from_attributes": True}


class DomainCreate(BaseModel):
    name: str
    full_url: str
    domain: str
    category_id: int


class DomainUpdate(BaseModel):
    name: Optional[str] = None
    full_url: Optional[str] = None
    domain: Optional[str] = None
    category_id: Optional[int] = None
