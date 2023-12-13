from typing import Dict, Union, List

from fastapi import APIRouter, Depends, Path, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app_fast.CRUD.tweets_crud import tweet_create, tweet_delete, get_tweets_feed
from app_fast.CRUD.users_crud import get_current_user_by_api_key
from app_fast.db_and_models.models import Tweet, User
from app_fast.db_and_models.schemas import TweetPydantic
from app_fast.db_and_models.session import get_async_session

router = APIRouter(tags=["Tweets"])


# Роут для создания нового твита
@router.post("/tweets", response_model=Dict[str, Union[bool, int]])
async def create_tweet(new_tweet: Tweet = Depends(tweet_create)):
    return await new_tweet.to_json()


@router.delete("/tweets/{tweet_id}", response_model=Dict[str, bool])
async def delete_tweet(
    tweet_id: int = Path(..., title="ID твита"),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_by_api_key),
):
    return await tweet_delete(
        tweet_id=tweet_id, session=session, current_user=current_user
    )


# Роут для получения ленты твитов
@router.get("/tweets", response_model=Dict[str, Union[bool, List[TweetPydantic]]])
async def get_tweets(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_by_api_key),
    page: int = Query(1, title="Page Number"),
    per_page: int = Query(10, title="Tweets Per Page"),
):
    tweets = await get_tweets_feed(
        session=session, current_user_id=current_user.id, page=page, per_page=per_page
    )
    if tweets is None:
        raise HTTPException(status_code=404, detail="No tweets found.")

    return {"result": True, "tweets": tweets}
