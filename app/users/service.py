from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext

from app.users.exceptions import UserNotFoundException, UserAlreadyExistsException
from app.users.repository import UserRepository
from app.users.schemas import UserCreateSchema, UserPublicSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self, repository: Annotated[UserRepository, Depends()]):
        self.repository = repository

    async def get(self, user_id: int) -> UserPublicSchema:
        try:
            return await self.repository.get(user_id)
        except ValueError:
            raise UserNotFoundException

    async def get_list(self) -> list[UserPublicSchema]:
        return await self.repository.get_list()

    async def get_by_username(self, username: str) -> UserPublicSchema:
        try:
            return await self.repository.get_by_username(username)
        except ValueError:
            raise UserNotFoundException

    async def create(self, user_create: UserCreateSchema) -> UserPublicSchema:
        try:
            return await self.repository.create(user_create)
        except ValueError:
            raise UserAlreadyExistsException

    async def update(self, user_id: int, user_update: UserCreateSchema) -> UserPublicSchema:
        try:
            return await self.repository.update(user_id, user_update)
        except ValueError:
            raise UserNotFoundException

    async def delete(self, user_id: int) -> None:
        try:
            return await self.repository.delete(user_id)
        except ValueError:
            raise UserNotFoundException
