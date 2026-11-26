import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest

from app import create_app, db
from app.models.user import User


@pytest.fixture
def app():
    app = create_app()

    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI="sqlite://",
    )

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_registration(client, app):
    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePassword123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(username="testuser").first()

        assert user is not None
        assert user.password_hash != "SecurePassword123!"


def test_login(client):
    client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePassword123!"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "SecurePassword123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Welcome, testuser!" in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logout(client):
    client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePassword123!"
        }
    )

    client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "SecurePassword123!"
        }
    )

    response = client.post("/logout")

    assert response.status_code == 302

    response = client.get("/dashboard")

    assert response.status_code == 302
