from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app_fast.db_and_models.models import Like, Tweet, User


async def like_tweet(
    tweet_id: int,
    session: AsyncSession,
    current_user: User,
):
    # Проверяем, является ли текущий пользователь автором твита
    tweet_author_id = await session.execute(
        select(Tweet.author_id).where(Tweet.id == tweet_id)
    )
    tweet_author_id = tweet_author_id.scalar()

    if current_user.id == tweet_author_id:
        return {
            "result": False,
            "error_type": "Self Like",
            "error_message": "You cannot like your own tweet",
        }

    # Проверяем, есть ли уже лайк от текущего пользователя для данного твита
    existing_like = await session.execute(
        select(Like).where(
            Like.user_id == current_user.id,
            Like.tweet_id == tweet_id,
        )
    )

    existing_like = existing_like.scalar()
    if existing_like is not None:
        return {
            "result": False,
            "error_type": "Already Liked",
            "error_message": "You've already liked this tweet",
        }

    like = Like(user_id=current_user.id, tweet_id=tweet_id)
    session.add(like)
    await session.commit()
    await session.refresh(like)

    return like


async def unlike_tweet(
    tweet_id: int,
    session: AsyncSession,
    current_user: User,
):
    # Проверяем, является ли текущий пользователь автором твита
    tweet_author_id = await session.execute(
        select(Tweet.author_id).where(Tweet.id == tweet_id)
    )
    tweet_author_id = tweet_author_id.scalar()

    if current_user.id == tweet_author_id:
        return {
            "result": False,
            "error_type": "Self Like",
            "error_message": "You cannot like your own tweet",
        }

    # Проверяем, существует ли "лайк" от текущего пользователя к данному твиту
    existing_like = await session.execute(
        select(Like).where(Like.user_id == current_user.id, Like.tweet_id == tweet_id)
    )

    existing_like = existing_like.scalar()
    if existing_like is None:
        raise HTTPException(status_code=400, detail="Лайк не существует")

    # Удаляем "лайк" из базы данных
    await session.delete(existing_like)
    await session.commit()

    return {"result": True}
