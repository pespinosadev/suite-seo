from typing import Optional
from pydantic import BaseModel


class SportEventIn(BaseModel):
    dia: str
    fecha: str
    deporte: str
    hora: str
    competicion: str
    evento: str
    canal: Optional[str] = None


class BatchEventsRequest(BaseModel):
    events: list[SportEventIn]


class SportEventOut(BaseModel):
    id: int
    day_name: str
    event_date: str
    deporte: str
    hora: str
    competicion: str
    evento: str
    canal: Optional[str]

    model_config = {"from_attributes": True}
