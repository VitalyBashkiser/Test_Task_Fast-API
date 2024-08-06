from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from post import schema, crud

router = APIRouter()


@router.get("/posts/", response_model=List[schema.PostInDB])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@router.post("/posts/", response_model=schema.PostInDB)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post)


@router.get("/posts/{post_id}", response_model=schema.PostInDB)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post_by_id(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/posts/{post_id}", response_model=schema.PostInDB)
def update_post(
    post_id: int, post: schema.PostUpdate, db: Session = Depends(get_db)
):
    db_post = crud.get_post_by_id(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.update_post(db, post_id, post)


@router.delete("/posts/{post_id}", response_model=schema.PostInDB)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post_by_id(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.delete_post(db, post_id)


@router.get("/comments/", response_model=List[schema.CommentInDB])
def read_comments(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    comments = crud.get_comments(db, skip=skip, limit=limit)
    return comments


@router.post("/comments/{post_id}", response_model=schema.CommentInDB)
def create_comment(
    post_id: int, comment: schema.CommentCreate, db: Session = Depends(get_db)
):
    return crud.create_comment(db, comment, post_id)


@router.get("/comments/{comment_id}", response_model=schema.CommentInDB)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment_by_id(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.put("/comments/{comment_id}", response_model=schema.CommentInDB)
def update_comment(
    comment_id: int,
    comment: schema.CommentUpdate,
    db: Session = Depends(get_db),
):
    db_comment = crud.get_comment_by_id(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return crud.update_comment(db, comment_id, comment)


@router.delete("/comments/{comment_id}", response_model=schema.CommentInDB)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment_by_id(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return crud.delete_comment(db, comment_id)


@router.get(
    "/comments-daily-breakdown", response_model=List[schema.CommentAnalytics]
)
def get_comments_daily_breakdown(
    date_from: datetime, date_to: datetime, db: Session = Depends(get_db)
):
    result = crud.get_comments_daily_breakdown(db, date_from, date_to)

    analytics = [
        {
            "date": f"{int(row.year)}-{int(row.month):02}-{int(row.day):02}",
            "total_comments": row.total_comments,
            "blocked_comments": row.blocked_comments,
        }
        for row in result
    ]

    return analytics
