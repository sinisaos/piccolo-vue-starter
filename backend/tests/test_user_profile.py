from fastapi.testclient import TestClient

from main import app


def test_current_user(test_db, create_test_data, create_access_token):
    client = TestClient(
        app, cookies={"Authorization": f"Bearer {create_access_token}"}
    )

    response = client.get("/accounts/profile/")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_current_user_tasks(test_db, create_test_data, create_access_token):
    client = TestClient(
        app, cookies={"Authorization": f"Bearer {create_access_token}"}
    )

    response = client.get("/accounts/profile/tasks/")
    assert response.status_code == 200
    assert response.json()[0]["task_user"] == 1
    assert len(response.json()) == 2
