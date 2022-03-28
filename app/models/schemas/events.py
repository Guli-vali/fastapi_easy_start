from typing import List

from app.models.domain.rwmodel import RWModel
from app.models.domain.events import Event


class EventInResponse(Event, RWModel):
    pass

class EventInCreate(RWModel):
    title: str
    location: str

class ListOfEventsInResponse(RWModel):
    events: List[EventInResponse]
    count: int
