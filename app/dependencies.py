from typing import Annotated

from fastapi import Security, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import SECRET_KEY, ALGORITHM
from app.database import AsyncSessionLocal
from app.users.schemas import UserPublicSchema


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()
        await session.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Security(oauth2_scheme)]) -> UserPublicSchema:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = UserPublicSchema(**payload)
    return user
