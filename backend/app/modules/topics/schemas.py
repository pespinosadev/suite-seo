import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class TopicCategoryCreate(BaseModel):
    name: str
    display_order: int = 0


class TopicCategoryOut(BaseModel):
    id: int
    name: str
    display_order: int
    is_fixed: bool
    model_config = {"from_attributes": True}


class DailyTopicCreate(BaseModel):
    title: str
    url: Optional[str] = None
    include_url: bool = False
    observation: Optional[str] = None
    category_id: Optional[int] = None
    original_source: Optional[str] = None
    original_url: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_max(cls, v: str) -> str:
        if len(v) > 200:
            raise ValueError("Máximo 200 caracteres")
        return v


class DailyTopicUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    include_url: Optional[bool] = None
    observation: Optional[str] = None
    category_id: Optional[int] = None


class AutoTopicCreate(BaseModel):
    title: str
    display_order: int = 0


class AutoTopicUpdate(BaseModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class AutoTopicOut(BaseModel):
    id: int
    title: str
    is_active: bool
    display_order: int
    model_config = {"from_attributes": True}


class DailyTopicOut(BaseModel):
    id: int
    title: str
    url: Optional[str]
    include_url: bool
    observation: Optional[str]
    category: Optional[TopicCategoryOut]
    original_source: Optional[str]
    original_url: Optional[str]
    created_at: datetime.datetime
    is_draft: bool
    sent_at: Optional[datetime.datetime]
    model_config = {"from_attributes": True}
