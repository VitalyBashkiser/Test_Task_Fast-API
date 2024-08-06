from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from main import app
from db.session import SessionLocal
from post import models

client = TestClient(app)


@pytest.fixture
def create_test_user():
    db = SessionLocal()
    user = models.User(email="test@example.com", username="testuser", hashed_password="hashedpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


@pytest.fixture
def create_test_post(create_test_user):
    db = SessionLocal()
    post = models.Post(title="Test Post", content="Test Content", user_id=create_test_user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    db.close()
    return post


def test_create_post(create_test_user):
    response = client.post(
        "/create/",
        json={
            "title": "New Post",
            "content": "Content of the new post",
            "user_id": create_test_user.id,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Post"
    assert data["content"] == "Content of the new post"


def test_read_posts():
    response = client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_post(create_test_post):
    response = client.get(f"/posts/{create_test_post.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == create_test_post.title


def test_update_post(create_test_post):
    response = client.put(
        f"/posts/{create_test_post.id}",
        json={"title": "Updated Title", "content": "Updated Content"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_delete_post(create_test_post):
    response = client.delete(f"/posts/{create_test_post.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == create_test_post.title


def test_create_comment(create_test_post, create_test_user):
    response = client.post(
        f"/comments/{create_test_post.id}",
        json={"content": "This is a comment", "user_id": create_test_user.id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "This is a comment"


def test_read_comments():
    response = client.get("/comments/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_comments_daily_breakdown():
    date_from = datetime.now().strftime("%Y-%m-%d")
    date_to = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = client.get(
        "/comments-daily-breakdown",
        params={"date_from": date_from, "date_to": date_to},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
