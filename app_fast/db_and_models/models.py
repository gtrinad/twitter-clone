from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from app_fast.db_and_models.engine import Base
from app_fast.db_and_models.schemas import (
    UserPydantic,
    UserProfile,
    UserProfileResponse,
)


# Модель данных для пользователя
class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True)
    password: str = Column(String)
    name: str = Column(String)
    email: str = Column(String)
    api_token: str = Column(String)

    tweets = relationship("Tweet", back_populates="author")
    likes = relationship("Like", back_populates="user")

    followers = relationship(
        "User",
        secondary="followers",
        primaryjoin="User.id == UserFollows.following_id",
        secondaryjoin="User.id == UserFollows.follower_id",
        back_populates="following",
        lazy="dynamic",
    )

    following = relationship(
        "User",
        secondary="followers",
        primaryjoin="User.id == UserFollows.follower_id",
        secondaryjoin="User.id == UserFollows.following_id",
        back_populates="followers",
        lazy="dynamic",
    )

    async def get_followers_data(self, session: AsyncSession):
        followers = await session.execute(
            select(User)
            .join(UserFollows, User.id == UserFollows.follower_id)
            .filter(UserFollows.following_id == self.id)
        )

        # Преобразуем результат запроса в список объектов UserPydantic
        followers_data = [
            UserPydantic(id=follower.id, name=follower.name)
            for follower in followers.scalars().all()
        ]

        return followers_data

    async def get_following_data(self, session: AsyncSession):
        followings = await session.execute(
            select(User)
            .join(UserFollows, User.id == UserFollows.following_id)
            .filter(UserFollows.follower_id == self.id)
        )

        # Преобразуем результат запроса в список объектов UserPydantic
        following_data = [
            UserPydantic(id=following.id, name=following.name)
            for following in followings.scalars().all()
        ]

        return following_data

    async def to_json(self, session: AsyncSession):
        followers = await self.get_followers_data(session=session)
        following = await self.get_following_data(session=session)

        user_profile = UserProfile(
            id=self.id,
            name=self.name,
            followers=followers,
            following=following,
        )

        user_profile_response = UserProfileResponse(result=True, user=user_profile)

        return user_profile_response.model_dump()


# Модель данных для твита
class Tweet(Base):
    __tablename__ = "tweets"

    id: int = Column(Integer, primary_key=True, index=True)
    tweet_data: str = Column(String)
    author_id: int = Column(Integer, ForeignKey("users.id"))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="tweets")
    likes = relationship("Like", back_populates="tweet")
    images = relationship(
        "PostImages", backref="post", lazy=True, cascade="all, delete-orphan"
    )

    async def to_json(self):
        return {
            "result": True,
            "tweet_id": self.id,
        }


# Модель данных для images
class Images(Base):
    __tablename__ = "images"

    id: int = Column(Integer, primary_key=True)
    url: str = Column(String)

    async def to_json(self):
        return {
            "image_id": self.id,
            "url": self.url,
        }


class PostImages(Base):
    __tablename__ = "post_images"

    id: int = Column(Integer, primary_key=True)
    tweet_id: int = Column(Integer, ForeignKey("tweets.id"))
    image_id: int = Column(Integer, ForeignKey("images.id"), nullable=False)

    image = relationship("Images")

    async def href(self) -> str:
        return f"/{self.image.url}"

    async def to_json(self) -> dict:
        return {
            "image_id": self.image_id,
            "tweet_id": self.tweet_id,
            "url": f"/{self.image.url}",
        }


# Модель данных для лайка
class Like(Base):
    __tablename__ = "likes"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    tweet_id: int = Column(Integer, ForeignKey("tweets.id"))

    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")

    __table_args__ = (UniqueConstraint("user_id", "tweet_id", name="_user_tweet_uc"),)


# Модель данных для фоловеров
class UserFollows(Base):
    __tablename__ = "followers"

    id: int = Column(Integer, primary_key=True, index=True)
    follower_id: int = Column(Integer, ForeignKey("users.id"))
    following_id: int = Column(Integer, ForeignKey("users.id"))
