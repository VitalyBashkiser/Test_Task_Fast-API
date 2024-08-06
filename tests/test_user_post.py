from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from main import app
from user.models import User
from post.models import Post, Comment

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def create_test_user():
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "testuser@example.com").first()
    if not user:
        user = User(
            email="testuser@example.com", hashed_password="hashedpassword123"
        )
        db.add(user)
        db.commit()
    db.close()

    response = client.post(
        "/user/login",
        json={"email": "testuser@example.com", "password": "testpassword"},
    )
    token = response.json().get("access_token")
    return user, token


def test_register_user(create_test_user):
    response = client.post(
        "/user/signup",
        json={"email": "uniqueuser@example.com", "password": "uniquepassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert (
        "access_token" in data or data.get("detail") == "Email already in use"
    )


def test_user_login(create_test_user):
    _, token = create_test_user
    response = client.post(
        "/user/login",
        json={"email": "uniqueuser@example.com", "password": "uniquepassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_create_new_post(create_test_user):
    _, token = create_test_user

    response = client.post(
        "/posts/",
        json={
            "title": "Sample Title",
            "content": "Sample Content",
            "user_id": 1,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["title"] == "Sample Title"
    assert data["content"] == "Sample Content"

    db = TestingSessionLocal()
    post = db.query(Post).filter(Post.title == "Sample Title").first()
    if post:
        db.delete(post)
        db.commit()
    db.close()


def test_comments_breakdown(create_test_user):
    user, token = create_test_user

    today_date = datetime.now().strftime("%Y-%m-%d")
    next_day_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    db = TestingSessionLocal()
    post = Post(title="Sample Post", content="Sample Content", user_id=user.id)
    db.add(post)

    comment1 = Comment(
        content="Positive comment",
        post_id=post.id,
        created_at=datetime.now(),
        blocked=False,
    )
    db.add(comment1)

    comment2 = Comment(
        content="Negative comment with inappropriate content",
        post_id=post.id,
        created_at=datetime.now(),
        blocked=True,
    )
    db.add(comment2)

    db.commit()

    comments = db.query(Comment).all()
    assert len(comments) >= 2

    response = client.get(
        "/comments-daily-breakdown",
        params={"date_from": today_date, "date_to": next_day_date},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "total_comments" in data[0]
    assert "blocked_comments" in data[0]
    assert data[0]["blocked_comments"] >= 1

    comment1 = (
        db.query(Comment).filter(Comment.content == "Positive comment").first()
    )
    if comment1:
        db.delete(comment1)

    comment2 = (
        db.query(Comment)
        .filter(
            Comment.content == "Negative comment with inappropriate content"
        )
        .first()
    )
    if comment2:
        db.delete(comment2)

    post = db.query(Post).filter(Post.title == "Sample Post").first()
    if post:
        db.delete(post)

    db.commit()
    db.close()


def test_access_protected_route(create_test_user):
    _, token = create_test_user

    response = client.get(
        "/posts/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_access_protected_route_without_token():
    response = client.get("/posts/")
    assert response.status_code == 403
