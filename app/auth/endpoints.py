from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.auth.schemas import UserCredentialsSchema
from app.auth.service import AuthService
from app.users.exceptions import InvalidCredentialsException, UserNotFoundException

router = APIRouter()


@router.post("/login", status_code=200, tags=['auth'])
async def login(
        credentials: UserCredentialsSchema,
        service: Annotated[AuthService, Depends()],
):
    try:
        return {
            "token": await service.generate_token(credentials)
        }
    except InvalidCredentialsException as e:
        code = {
            UserNotFoundException: 404,
            InvalidCredentialsException: 401
        }[type(e)]
        raise HTTPException(detail=str(e), status_code=code)
