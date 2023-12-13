import asyncio

import pytest
from httpx import AsyncClient

from app_fast.db_and_models.engine import async_engine, Base
from app_fast.db_and_models.models import User

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_fast.main import create_app


@pytest.fixture(scope="session")
async def app():
    app = create_app()
    app.state.TESTING = True

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        users_to_insert = [
            {
                "username": "username_1",
                "password": "password_1",
                "name": "name_1",
                "email": "email_1@example.com",
                "api_token": "token_1",
            },
            {
                "username": "username_2",
                "password": "password_2",
                "name": "name_2",
                "email": "email_2@example.com",
                "api_token": "token_2",
            },
        ]
        await conn.execute(User.__table__.insert().values(users_to_insert))

    yield app

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def client(app: create_app) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
