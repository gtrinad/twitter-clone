from app_fast.db_and_models.engine import (
    AsyncSessionLocal,
    Base,
    async_engine,
)


# Функция для получения асинхронной сессии базы данных
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session


# Асинхронная функция для создания базы данных и таблиц
async def create_async_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
