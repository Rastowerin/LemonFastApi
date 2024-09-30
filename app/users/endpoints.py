from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.users.models import User
from app.users.schemas import UserCreateSchema, UserPublicSchema
from app.users.service import UserService

router = APIRouter()


@router.get("/users/{user_id}", response_model=UserPublicSchema, status_code=200, tags=['users'])
async def get(
        user_id: int,
        service: Annotated[UserService, Depends()],
        current_user: User = Depends(get_current_user)
):
    return await service.get(user_id)


@router.get("/users", response_model=list[UserPublicSchema], status_code=200, tags=['users'])
async def get_list(
        service: Annotated[UserService, Depends()],
        current_user: User = Depends(get_current_user)
):
    return await service.get_list()


@router.post("/users", response_model=UserPublicSchema, status_code=201, tags=['users'])
async def post(
        user: UserCreateSchema,
        service: Annotated[UserService, Depends()]
):
    return await service.create(user)


@router.put("/users/{user_id}", response_model=UserPublicSchema, status_code=200, tags=['users'])
async def put(
        user_id: int,
        user: UserCreateSchema,
        service: Annotated[UserService, Depends()],
        current_user: User = Depends(get_current_user)
):
    return await service.update(user_id, user)


@router.delete("/users/{user_id}", status_code=204, tags=['users'])
async def delete(
        user_id: int,
        service: Annotated[UserService, Depends()],
        current_user: User = Depends(get_current_user)
):
    await service.delete(user_id)
