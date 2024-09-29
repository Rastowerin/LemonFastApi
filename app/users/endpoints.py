from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.users.models import User
from app.users.schemas import UserCreateSchema, UserPublicSchema
from app.users.repository import UserRepository

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserPublicSchema, status_code=200, tags=['users'])
async def get(
        user_id: int,
        repository: Annotated[UserRepository, Depends()],
        current_user: User = Depends(get_current_user)
):
    return await repository.get(user_id)


@router.get("/users", response_model=list[UserPublicSchema], status_code=200, tags=['users'])
async def get_list(
        repository: Annotated[UserRepository, Depends()],
        current_user: User = Depends(get_current_user)
):
    return await repository.get_list()


@router.post("/users", response_model=UserPublicSchema, status_code=201, tags=['users'])
async def post(
        user: UserCreateSchema,
        repository: Annotated[UserRepository, Depends()]
):
    return await repository.create(user)


@router.put("/users/{user_id}", response_model=UserPublicSchema, status_code=200, tags=['users'])
async def put(
        user_id: int,
        user: UserCreateSchema,
        repository: Annotated[UserRepository, Depends()],
        current_user: User = Depends(get_current_user)
):
    return await repository.update(user_id, user)


@router.delete("/users/{user_id}", status_code=204, tags=['users'])
async def delete(
        user_id: int,
        repository: Annotated[UserRepository, Depends()],
        current_user: User = Depends(get_current_user)
):
    await repository.delete(user_id)
