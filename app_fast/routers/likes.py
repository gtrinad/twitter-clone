from fastapi import APIRouter, HTTPException, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app_fast.CRUD.likes_crud import like_tweet, unlike_tweet
from app_fast.CRUD.users_crud import get_current_user_by_api_key
from app_fast.db_and_models.models import User
from app_fast.db_and_models.schemas import LikeResponse
from app_fast.db_and_models.session import get_async_session

router = APIRouter(tags=["likes"])


# Создание эндпоинта для постановки "лайка" на твит
@router.post("/tweets/{tweet_id}/likes", response_model=LikeResponse)
async def like_tweet_endpoint(
    tweet_id: int = Path(..., title="ID твита"),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_by_api_key),
):
    try:
        liked_tweet = await like_tweet(
            tweet_id=tweet_id, session=session, current_user=current_user
        )
        if liked_tweet:
            return {"result": True}
        else:
            raise HTTPException(
                status_code=400, detail="Не удалось поставить лайк твиту"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


# Создание эндпоинта для снятия "лайка" с твита
@router.delete("/tweets/{tweet_id}/likes", response_model=LikeResponse)
async def unlike_tweet_endpoint(
    tweet_id: int = Path(..., title="ID твита"),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_by_api_key),
):
    return await unlike_tweet(
        tweet_id=tweet_id, session=session, current_user=current_user
    )
