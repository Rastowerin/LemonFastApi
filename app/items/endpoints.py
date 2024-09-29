from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.items.schemas import ItemSchema
from app.items.repository import ItemRepository
from app.users.schemas import UserPublicSchema

router = APIRouter()


@router.get("/items/{item_id}", response_model=ItemSchema, status_code=200, tags=['items'])
async def get(
        item_id: int,
        repository: Annotated[ItemRepository, Depends()],
        current_user: UserPublicSchema = Depends(get_current_user)
):
    return await repository.get(item_id)


@router.get("/items", response_model=list[ItemSchema], status_code=200, tags=['items'])
async def get(
        repository: Annotated[ItemRepository, Depends()],
        current_user: UserPublicSchema = Depends(get_current_user)
):
    return await repository.get_list()


@router.post("/items", response_model=ItemSchema, status_code=201, tags=['items'])
async def post(
        item: ItemSchema,
        repository: Annotated[ItemRepository, Depends()],
        current_user: UserPublicSchema = Depends(get_current_user)
):
    return await repository.create(item)


@router.delete("/items/{item_id}", status_code=204, tags=['items'])
async def delete(
        item_id: int,
        repository: Annotated[ItemRepository, Depends()],
        current_user: UserPublicSchema = Depends(get_current_user)
):
    return await repository.delete(item_id)


@router.put("/items/{item_id}", response_model=ItemSchema, status_code=200, tags=['items'])
async def put(
        item_id: int,
        item: ItemSchema,
        repository: Annotated[ItemRepository, Depends()],
        current_user: UserPublicSchema = Depends(get_current_user)
):
    return await repository.update(item_id, item)
