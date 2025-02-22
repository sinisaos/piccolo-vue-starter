from fastapi.testclient import TestClient
from piccolo.apps.user.tables import BaseUser

from main import app


def test_user_register(test_db, create_test_data):
    client = TestClient(app)
    payload = {
        "username": "user",
        "email": "user@user.com",
        "password": "user123",
        "active": True,
    }

    response = client.post(
        "/accounts/register/",
        json=payload,
    )
    assert response.status_code == 200
    assert response.json()["username"] == "user"


def test_register_failed(test_db, create_test_data):
    client = TestClient(app)
    payload = {
        "username": "testuser",
        "email": "testuser@user.com",
        "password": "testuser123",
        "active": True,
    }

    response = client.post(
        "/accounts/register/",
        json=payload,
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": "User with that email or username already exists.",
    }


def test_login(test_db, create_test_data):
    client = TestClient(app)
    payload = {
        "username": "testuser",
        "password": "testuser123",
    }

    response = client.post(
        "/accounts/login/",
        data=payload,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_login_failed(test_db, create_test_data):
    client = TestClient(app)
    payload = {
        "username": "wronguser",
        "password": "wronguser123",
    }

    response = client.post(
        "/accounts/login/",
        data=payload,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_logout(test_db, create_test_data, create_access_token):
    client = TestClient(
        app, cookies={"Authorization": f"Bearer {create_access_token}"}
    )

    response = client.get("/accounts/logout/")

    assert response.status_code == 204
    assert len(response.cookies) == 0


def test_delete_user(test_db, create_test_data, create_access_token):
    client = TestClient(
        app, cookies={"Authorization": f"Bearer {create_access_token}"}
    )

    response = client.delete("/accounts/delete/")

    users = BaseUser.select().run_sync()

    assert response.status_code == 204
    assert len(users) == 0
    assert len(response.cookies) == 0
