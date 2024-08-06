from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from user.models import User
from base import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
    blocked = Column(Boolean, default=False)
    auto_reply_enabled = Column(Boolean, default=False)
    auto_reply_delay = Column(Integer, default=5)
    comments = relationship(
        "Comment", order_by="Comment.id", back_populates="post"
    )


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")
    blocked = Column(Boolean, default=False)
    created_at = Column(DateTime)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)


User.posts = relationship("Post", order_by=Post.id, back_populates="user")
Post.comments = relationship(
    "Comment", order_by=Comment.id, back_populates="post"
)
