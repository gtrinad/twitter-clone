from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://admin:admin@postgres:5432/twitter_db"

# Создаём асинхронный engine
async_engine: AsyncEngine = create_async_engine(
    url=DATABASE_URL,
    echo=False,
)

# Создаём асинхронную сессию
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()
