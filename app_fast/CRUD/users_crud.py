from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app_fast.db_and_models.models import User
from app_fast.db_and_models.schemas import UserCreate
from app_fast.db_and_models.session import get_async_session


async def create_user_by_api_key(
    user_data: UserCreate,
    api_key: str = Header(...),
    session: AsyncSession = Depends(get_async_session),
):
    if api_key is None:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Создание нового пользователя
    new_user = User(
        username=user_data.username,
        password=user_data.password,
        name=user_data.name,
        email=user_data.email,
        api_token=user_data.api_token,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def get_current_user_by_api_key(
    api_key: str = Header(...), session: AsyncSession = Depends(get_async_session)
):
    if api_key is None:
        raise HTTPException(status_code=403, detail="Unauthorized")

    stmt = select(User).where(User.api_token == api_key)
    user_data = await session.execute(stmt)
    user = user_data.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    user_data = await session.execute(select(User).where(User.id == user_id))
    user = user_data.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
