from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app_fast.db_and_models.models import UserFollows


async def follow_user(
    follower_id: int,
    following_id: int,
    session: AsyncSession,
):
    # Проверка, не фоловит ли пользователь сам себя
    if follower_id == following_id:
        return False

    # Проверка, существует ли уже фоловинг между пользователями
    existing_follow = await session.execute(
        select(UserFollows).where(
            UserFollows.follower_id == follower_id,
            UserFollows.following_id == following_id,
        )
    )
    existing_follow = existing_follow.scalar()
    if existing_follow is not None:
        return False

    # Создаём новую запись в таблице followers
    new_follow = UserFollows(follower_id=follower_id, following_id=following_id)
    session.add(new_follow)
    await session.commit()

    return True


async def unfollow_user(
    current_user_id: int,
    user_to_unfollow_id: int,
    session: AsyncSession,
):
    # Попробуем найти запись о подписке
    existing_follow = await session.execute(
        select(UserFollows).where(
            UserFollows.follower_id == current_user_id,
            UserFollows.following_id == user_to_unfollow_id,
        )
    )
    existing_follow = existing_follow.scalar()
    if existing_follow is None:
        return False

    # Если запись о подписке существует, удаляем её
    await session.delete(existing_follow)
    await session.commit()

    return True
