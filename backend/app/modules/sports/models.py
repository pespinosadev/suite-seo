import datetime
from typing import Optional
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base


class SportEvent(Base):
    __tablename__ = "sport_events"

    id:          Mapped[int]           = mapped_column(primary_key=True)
    day_name:    Mapped[str]           = mapped_column(String(20))
    event_date:  Mapped[str]           = mapped_column(String(50))
    deporte:     Mapped[str]           = mapped_column(String(50))
    hora:        Mapped[str]           = mapped_column(String(10))
    competicion: Mapped[str]           = mapped_column(String(200))
    evento:      Mapped[str]           = mapped_column(String(500))
    canal:       Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at:  Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
