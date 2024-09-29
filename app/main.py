import uvicorn
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.exceptions import BadRequestException
from app.users.endpoints import router as users_router
from app.auth.endpoints import router as auth_router
from app.items.endpoints import router as item_router


app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(item_router)


@app.exception_handler(BadRequestException)
async def unicorn_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=exc.status,
        content={"message": str(exc)},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
