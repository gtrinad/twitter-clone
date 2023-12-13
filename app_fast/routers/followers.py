from fastapi import APIRouter, Path, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app_fast.CRUD.followers_crud import follow_user, unfollow_user
from app_fast.CRUD.users_crud import get_current_user_by_api_key
from app_fast.db_and_models.models import User
from app_fast.db_and_models.schemas import FollowResponse
from app_fast.db_and_models.session import get_async_session

router = APIRouter(tags=["Followers"])


@router.post("/users/{user_id}/follow", response_model=FollowResponse)
async def follow_user_endpoint(
    user_id: int = Path(..., title="User ID"),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_by_api_key),
):
    result = await follow_user(
        session=session, follower_id=current_user.id, following_id=user_id
    )
    if result is not None:
        return {"result": True}
    else:
        raise HTTPException(
            status_code=400, detail="Не удалось зафоловить пользователя"
        )


@router.delete("/users/{user_id}/follow", response_model=FollowResponse)
async def unfollow_user_endpoint(
    user_id: int = Path(..., title="User ID"),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_by_api_key),
):
    # Вызов функции unfollow_user, чтобы отменить подписку
    result = await unfollow_user(
        session=session, current_user_id=current_user.id, user_to_unfollow_id=user_id
    )
    if result is not None:
        return {"result": True}
    else:
        raise HTTPException(
            status_code=400, detail="Не удалось отписаться от пользователя"
        )
