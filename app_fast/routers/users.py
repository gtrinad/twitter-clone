from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app_fast.CRUD.users_crud import (
    get_current_user_by_api_key,
    get_user_by_id,
    create_user_by_api_key,
)
from app_fast.db_and_models.models import User
from app_fast.db_and_models.schemas import UserProfileResponse
from app_fast.db_and_models.session import get_async_session

router = APIRouter(tags=["Users"])


# Роут для создания нового пользователя
@router.post("/users", response_model=UserProfileResponse)
async def create_user(
    new_user: User = Depends(create_user_by_api_key),
    session: AsyncSession = Depends(get_async_session),
):
    return await new_user.to_json(session=session)


# Получить информацию о себе
@router.get("/users/me", response_model=UserProfileResponse)
async def get_current_user(
    current_user: User = Depends(get_current_user_by_api_key),
    session: AsyncSession = Depends(get_async_session),
):
    return await current_user.to_json(session=session)


# Получить информацию о произвольном пользователе по его id
@router.get("/users/{user_id}", response_model=UserProfileResponse)
async def get_user(
    current_user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    return await current_user.to_json(session=session)
