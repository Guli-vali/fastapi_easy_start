from pydantic import BaseConfig, BaseModel


class RWModel(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
