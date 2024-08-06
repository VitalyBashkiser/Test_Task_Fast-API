from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int
    auto_reply_enabled: bool = False
    auto_reply_delay: int = 5


class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]


class PostInDB(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str
    user_id: int


class CommentUpdate(BaseModel):
    content: Optional[str]
    blocked: bool


class CommentInDB(BaseModel):
    id: int
    post_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CommentAnalytics(BaseModel):
    date: str
    total_comments: int
    blocked_comments: int


class AutoReplySettingsUpdate(BaseModel):
    delay: int
    enabled: bool
