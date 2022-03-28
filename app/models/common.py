from pydantic import BaseModel, Field


class IDModelMixin(BaseModel):
    id_: int = Field(0, alias="id")
