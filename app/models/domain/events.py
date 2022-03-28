from app.models.domain.rwmodel import RWModel
from app.models.common import IDModelMixin


class Event(IDModelMixin, RWModel):
    title: str
    location: str
