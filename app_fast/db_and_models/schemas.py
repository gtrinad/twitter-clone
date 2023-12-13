from typing import List, Optional

from pydantic import BaseModel, EmailStr


# Базовая модель данных для пользователя
class UserPydantic(BaseModel):
    id: int
    name: str


# Модель данных для пользователя (для возвращаемых данных)
class UserProfile(BaseModel):
    id: int
    name: str
    followers: List[UserPydantic]
    following: List[UserPydantic]


class UserProfileResponse(BaseModel):
    result: bool
    user: UserProfile


# Модель данных для создания нового пользователя
class UserCreate(BaseModel):
    username: str
    password: str

    name: str
    email: EmailStr
    api_token: str


# Модель для создания твита
class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None


class LikeResponse(BaseModel):
    result: bool


class FollowResponse(BaseModel):
    result: bool


class ImagesResponse(BaseModel):
    result: bool
    media_id: int


class UserLikePydantic(BaseModel):
    user_id: int
    name: str


class TweetResponse(BaseModel):
    content: str
    attachments: List[str]
    author: UserPydantic
    likes: List[UserLikePydantic]


class TweetPydantic(TweetResponse):
    id: int
