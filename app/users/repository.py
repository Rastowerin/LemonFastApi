from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.users.exceptions import UserNotFoundException, UserAlreadyExistsException
from app.users.models import User
from app.users.schemas import UserCreateSchema, UserDBSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get_list(self) -> list[User]:
        result = await self.session.execute(
            select(User)
        )

        return list(result.scalars().all())

    async def get(self, user_id: int) -> User:
        user = await self.session.get(User, user_id)

        if user is None:
            raise UserNotFoundException

        return user

    async def get_by_username(self, username: str) -> User:
        user = await self.session.execute(
            select(User).where(User.username == username)
        )

        if user is None:
            raise UserNotFoundException

        return user.scalar()

    async def create(self, user_create: UserCreateSchema) -> User:
        hashed_password = pwd_context.hash(user_create.password)
        user = User(**user_create.model_dump(exclude='password'), hashed_password=hashed_password)
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        except IntegrityError:
            raise UserAlreadyExistsException
        return user

    async def update(self, user_id: int, user_update: UserCreateSchema) -> User:

        check = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        if not check.scalar():
            raise UserNotFoundException

        hashed_password = pwd_context.hash(user_update.password)
        user = UserDBSchema(**user_update.model_dump(exclude='password'), hashed_password=hashed_password)

        await self.session.execute(
            update(User).where(User.id == user_id).values(**user.model_dump())
        )
        user = await self.session.get(User, user_id)

        return user

    async def delete(self, user_id: int) -> None:

        check = await self.session.execute(
            select(User).where(User.id == user_id)
        )

        if not check.scalar():
            raise UserNotFoundException

        await self.session.execute(
            delete(User).where(User.id == user_id)
        )
