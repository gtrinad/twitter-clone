from typing import List

from fastapi import Depends
from sqlalchemy import or_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, aliased

from app_fast.CRUD.users_crud import get_current_user_by_api_key
from app_fast.db_and_models.models import (
    User,
    Tweet,
    Images,
    PostImages,
    UserFollows,
    Like,
)
from app_fast.db_and_models.schemas import TweetCreate, TweetPydantic
from app_fast.db_and_models.session import get_async_session


async def tweet_create(
    tweet_data: TweetCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_by_api_key),
):
    # Создаём новый твит
    new_tweet = Tweet(tweet_data=tweet_data.tweet_data, author_id=current_user.id)

    session.add(new_tweet)
    await session.commit()
    await session.refresh(new_tweet)

    # Если указаны media_ids, связываем их с твитом
    if tweet_data.tweet_media_ids:
        for media_id in tweet_data.tweet_media_ids:
            image = await session.execute(select(Images).where(Images.id == media_id))
            image = image.scalar()
            if image:
                post_image = PostImages(tweet_id=new_tweet.id, image_id=image.id)
                session.add(post_image)

        await session.commit()

    return new_tweet


async def tweet_delete(tweet_id: int, session: AsyncSession, current_user: User):
    # Проверяем, что пользователь удаляет свой собственный твит
    tweet = await session.execute(
        select(Tweet).where(Tweet.id == tweet_id, Tweet.author_id == current_user.id)
    )
    tweet = tweet.scalar()
    if tweet is None:
        return {
            "result": False,
            "error_type": "Unauthorized",
            "error_message": "You can only delete your own tweets",
        }

    # Удалить твит
    await session.delete(tweet)
    await session.commit()

    return {"result": True}


async def get_tweets_feed(
    current_user_id: int, page: int, per_page: int, session: AsyncSession
) -> List[TweetPydantic]:
    # Выполняем запрос, чтобы получить твиты для ленты пользователя,
    # включая твиты пользователей, на которых подписан текущий пользователь.
    subquery = select(UserFollows.following_id).where(
        UserFollows.follower_id == current_user_id
    )
    following_ids = await session.execute(subquery)
    following_ids = following_ids.scalars().all()

    like_alias = aliased(Like)

    tweets = await session.execute(
        select(Tweet, func.count(like_alias.id).label("like_count"))
        .outerjoin(like_alias, Tweet.likes)
        .options(
            joinedload(Tweet.author),  # Load the author relationship
            joinedload(Tweet.likes).joinedload(
                Like.user
            ),  # Load the likes relationship
            joinedload(Tweet.images).joinedload(
                PostImages.image
            ),  # Load the images relationship
        )
        .filter(
            or_(Tweet.author_id == current_user_id, Tweet.author_id.in_(following_ids))
        )
        .group_by(Tweet.id)
        .order_by(desc("like_count"), Tweet.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )

    # Вызываем unique() после всех операций с соединенными загрузками
    tweets = tweets.unique()

    # Теперь можно получить результаты
    tweets = tweets.scalars().all()

    # Преобразуем твиты в формат, который будет возвращен в ответе.
    tweet_list = [
        TweetPydantic(
            id=tweet.id,
            content=tweet.tweet_data,
            attachments=[await attachment.href() for attachment in tweet.images],
            author={"id": tweet.author.id, "name": tweet.author.name},
            likes=[
                {"user_id": like.user_id, "name": like.user.name}
                for like in tweet.likes
            ],
        )
        for tweet in tweets
    ]

    return tweet_list
