from typing import Annotated

from fastapi import Depends
from app.items.repository import ItemRepository
from app.items.schemas import ItemSchema


class ItemService:

    def __init__(self, repository: Annotated[ItemRepository, Depends()]):
        self.repository = repository

    async def get(self, item_id: int) -> ItemSchema:
        return await self.repository.get(item_id)

    async def get_list(self) -> list[ItemSchema]:
        return await self.repository.get_list()

    async def create(self, item_schema: ItemSchema) -> ItemSchema:
        return await self.repository.create(item_schema)

    async def update(self, item_id: int, item_schema: ItemSchema) -> ItemSchema:
        return await self.repository.update(item_id, item_schema)

    async def delete(self, item_id: int) -> None:
        return await self.repository.delete(item_id)
