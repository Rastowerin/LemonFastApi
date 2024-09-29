from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.items.exceptions import ItemNotFoundException, ItemAlreadyExistsException
from app.items.models import Item
from app.items.schemas import ItemSchema


class ItemRepository:

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get(self, item_id: int) -> Item:
        result = await self.session.get(Item, item_id)

        if result is None:
            raise ItemNotFoundException

        return result

    async def get_list(self) -> list[Item]:
        result = await self.session.execute(
            select(Item)
        )
        return list(result.scalars().all())

    async def create(self, item_schema: ItemSchema) -> Item:

        item = Item(**item_schema.model_dump())
        try:
            self.session.add(item)
            await self.session.commit()
            await self.session.refresh(item)
        except IntegrityError:
            raise ItemAlreadyExistsException
        return item

    async def update(self, item_id: int, item_schema: ItemSchema) -> Item:

        check = await self.session.execute(
            select(Item).where(Item.id == item_id)
        )

        if not check.scalar():
            raise ItemNotFoundException

        await self.session.execute(
            update(Item).where(Item.id == item_id).values(**item_schema.model_dump(exclude_unset=True))
        )
        item = Item(**item_schema.model_dump())
        return item

    async def delete(self, item_id: int) -> None:

        check = await self.session.execute(
            select(Item).where(Item.id == item_id)
        )

        if not check.scalar():
            raise ItemNotFoundException

        await self.session.execute(
            delete(Item).where(Item.id == item_id)
        )
