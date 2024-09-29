from typing import Annotated

from fastapi import Depends
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.auth.schemas import UserCredentialsSchema
from app.config import SECRET_KEY, ALGORITHM
from app.users.exceptions import UserNotFoundException, InvalidCredentialsException
from app.users.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    def __init__(self, user_repository: Annotated[UserRepository, Depends()]):
        self.user_repository = user_repository

    async def generate_token(self, credentials: UserCredentialsSchema) -> str:

        try:
            user = await self.user_repository.get_by_username(credentials.username)
        except UserNotFoundException:
            raise InvalidCredentialsException

        if not pwd_context.verify(hash=user.hashed_password, secret=credentials.password):
            raise InvalidCredentialsException

        to_encode = {
            "id": user.id,
            "username": user.username,
        }

        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
