from datetime import datetime, date

from sqlalchemy import extract, func, Integer
from sqlalchemy.orm import Session

from post import models
from post import schema
from post.models import Comment
from post.utils import schedule_auto_reply
from post.gemmeni import HARM_PROBABILITY, MODEL
from dotenv import load_dotenv

load_dotenv()


def check_content_moderation(comment_text: str) -> bool:
    response = MODEL.generate_content(comment_text)

    response_str = str(response)

    contains_harmful_content = any(
        category in response_str for category in HARM_PROBABILITY
    )

    if contains_harmful_content:
        return False

    return True


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def create_post(db: Session, post: schema.PostCreate):
    blocked_status = False

    if not check_content_moderation(post.content):
        blocked_status = True
    if not check_content_moderation(post.title):
        blocked_status = True

    db_post = models.Post(**post.dict(), blocked=blocked_status)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post: schema.PostUpdate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    for field, value in post.dict(exclude_unset=True).items():
        setattr(db_post, field, value)
    db.commit()
    # TODO: add moderation if needed
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return db_post


def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(skip).limit(limit).all()


def get_comment_by_id(db: Session, comment_id: int):
    return (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .first()
    )


def create_comment(
    db: Session,
    comment: schema.CommentCreate,
    post_id: int,
    parent_id: int = None,
):
    current_time = datetime.utcnow()
    blocked_status = False

    if not check_content_moderation(comment.content):
        blocked_status = True

    db_comment = models.Comment(
        **comment.dict(),
        blocked=blocked_status,
        post_id=post_id,
        created_at=current_time,
        parent_id=parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    post = db.query(models.Post).get(post_id)
    if post.auto_reply_enabled:
        schedule_auto_reply(post, db_comment)

    return db_comment


def update_comment(
    db: Session, comment_id: int, comment: schema.CommentUpdate
):
    db_comment = (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .first()
    )
    for field, value in comment.dict(exclude_unset=True).items():
        setattr(db_comment, field, value)
    db.commit()
    # TODO: add moderation if needed
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = (
        db.query(models.Comment)
        .filter(models.Comment.id == comment_id)
        .first()
    )
    db.delete(db_comment)
    db.commit()
    return db_comment


def get_comments_daily_breakdown(db: Session, date_from: date, date_to: date):
    result = (
        db.query(
            extract("day", Comment.created_at).label("day"),
            extract("month", Comment.created_at).label("month"),
            extract("year", Comment.created_at).label("year"),
            func.count().label("total_comments"),
            func.sum(func.cast(Comment.blocked, Integer)).label(
                "blocked_comments"
            ),
        )
        .filter(Comment.created_at.between(date_from, date_to))
        .group_by("year", "month", "day")
        .order_by("year", "month", "day")
        .all()
    )
    return result
