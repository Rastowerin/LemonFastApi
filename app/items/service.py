from typing import Annotated

from fastapi import Depends

from app.items.exceptions import ItemNotFoundException, ItemAlreadyExistsException
from app.items.repository import ItemRepository
from app.items.schemas import ItemSchema


class ItemService:

    def __init__(self, repository: Annotated[ItemRepository, Depends()]):
        self.repository = repository

    async def get(self, item_id: int) -> ItemSchema:
        try:
            return await self.repository.get(item_id)
        except ValueError:
            raise ItemNotFoundException

    async def get_list(self) -> list[ItemSchema]:
        return await self.repository.get_list()

    async def create(self, item_schema: ItemSchema) -> ItemSchema:
        try:
            return await self.repository.create(item_schema)
        except ValueError:
            raise ItemAlreadyExistsException

    async def update(self, item_id: int, item_schema: ItemSchema) -> ItemSchema:
        try:
            return await self.repository.update(item_id, item_schema)
        except ValueError:
            raise ItemNotFoundException

    async def delete(self, item_id: int) -> None:
        try:
            return await self.repository.delete(item_id)
        except ValueError:
            raise ItemNotFoundException
