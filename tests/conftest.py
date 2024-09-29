import asyncio

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from app.database import Base
from app.dependencies import get_db, get_current_user
from app.main import app
from app.users.models import User

DATABASE_URL_TEST = 'sqlite+aiosqlite:///:memory:'

engine = create_async_engine(DATABASE_URL_TEST)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope='session')
def client():
    async def override_get_db() -> AsyncSession:
        async with AsyncSessionLocal() as session:
            yield session
            await session.commit()
            await session.close()

    async def override_get_current_user() -> User:
        return User(
            id=1,
            username='test',
            hashed_password='<PASSWORD>',
        )

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    return TestClient(app)


@pytest.fixture(scope='function')
def reset_db():

    async def create_test_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(create_test_db())
