from pydantic import BaseModel, ConfigDict


class ItemSchema(BaseModel):
    id: int
    position: int
    author: str
    title: str
    views: int

    model_config = ConfigDict(from_attributes=True)
