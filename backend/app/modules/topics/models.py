import datetime
from typing import Optional
from sqlalchemy import String, Boolean, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base


class EmailLog(Base):
    __tablename__ = "email_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    sent_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    sender_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    sender_email: Mapped[str] = mapped_column(String(255), nullable=False)
    recipients: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    html_body: Mapped[str] = mapped_column(Text, nullable=False)
    topic_count: Mapped[int] = mapped_column(Integer, default=0)


class AutoTopic(Base):
    __tablename__ = "auto_topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)


class TopicCategory(Base):
    __tablename__ = "topic_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_fixed: Mapped[bool] = mapped_column(Boolean, default=False)
    topics: Mapped[list["DailyTopic"]] = relationship("DailyTopic", back_populates="category")


class DailyTopic(Base):
    __tablename__ = "daily_topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(1000))
    include_url: Mapped[bool] = mapped_column(Boolean, default=False)
    observation: Mapped[Optional[str]] = mapped_column(Text)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("topic_categories.id"), nullable=True)
    category: Mapped[Optional["TopicCategory"]] = relationship("TopicCategory", back_populates="topics")
    original_source: Mapped[Optional[str]] = mapped_column(String(100))
    original_url: Mapped[Optional[str]] = mapped_column(String(1000))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_draft: Mapped[bool] = mapped_column(Boolean, default=True)
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))
