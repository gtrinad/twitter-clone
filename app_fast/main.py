import uvicorn
from fastapi import FastAPI

from app_fast.db_and_models.engine import AsyncSessionLocal
from app_fast.db_and_models.models import User
from app_fast.db_and_models.session import create_async_db_and_tables
from app_fast.routers.users import router as user_router
from app_fast.routers.tweets import router as tweet_router
from app_fast.routers.likes import router as like_router
from app_fast.routers.followers import router as follow_router
from app_fast.routers.media import router as media_router
from sqlalchemy.future import select


def create_app():
    app = FastAPI(
        title="Twitter Clone app",
        description="Python Advanced Diploma",
        version="1.0.0",
        contact={"name": "admin", "email": "admin@gmail.com"},
    )

    app.include_router(user_router, prefix="/api")
    app.include_router(tweet_router, prefix="/api")
    app.include_router(like_router, prefix="/api")
    app.include_router(follow_router, prefix="/api")
    app.include_router(media_router, prefix="/api")

    async def startup_event():
        # Create database tables
        await create_async_db_and_tables()

        # Create a test user
        async with AsyncSessionLocal() as session:
            async with session.begin():
                test_user = User(
                    username="test_user",
                    password="test_password",
                    name="Test User",
                    email="test@example.com",
                    api_token="test",
                )
                session.add(test_user)

    app.add_event_handler("startup", startup_event)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug",
    )
