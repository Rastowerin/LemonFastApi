from pydantic import BaseModel


class ItemSchema(BaseModel):
    id: int
    position: int
    author: str
    title: str
    views: int
