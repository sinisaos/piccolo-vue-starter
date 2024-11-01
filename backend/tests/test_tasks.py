from fastapi.testclient import TestClient

from apps.tasks.tables import Task
from main import app


def test_get_all_tasks(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()["rows"]) == 2


def test_get_single_task(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/tasks/1/")
    assert response.status_code == 200
    assert response.json()["name"] == "Test task one"


def test_get_record_not_found(test_db, create_test_data):
    client = TestClient(app)
    response = client.get("/tasks/10/")
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"


def test_create_task(test_db, create_test_data, create_access_token):
    client = TestClient(
        app, cookies={"Authorization": f"Bearer {create_access_token}"}
    )

    payload = {
        "name": "Test task three",
        "created_at": "2024-03-10T16:38:01",
        "completed": False,
        "task_user": 1,
    }
    response = client.post("/tasks/", json=payload)
    result = (
        Task.select(Task.name)
        .where(Task._meta.primary_key == response.json()[0]["id"])
        .run_sync()
    )
    assert response.status_code == 201
    assert result[0]["name"] == "Test task three"


def test_update_task(test_db, create_test_data, create_access_token):
    client = TestClient(
        app, cookies={"Authorization": f"Bearer {create_access_token}"}
    )

    payload = {
        "name": "Updated test task two",
    }
    response = client.patch("/tasks/2/", json=payload)
    assert response.status_code == 200

    response = client.get("/tasks/2/")
    assert response.status_code == 200
    assert response.json()["name"] == "Updated test task two"


def test_update_record_not_found(
    test_db, create_test_data, create_access_token
):
    client = TestClient(
        app, cookies={"Authorization": f"Bearer {create_access_token}"}
    )

    payload = {
        "name": "Updated test task two",
    }

    response = client.patch("/tasks/10/", json=payload)
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"


def test_delete_task(test_db, create_test_data, create_access_token):
    client = TestClient(
        app, cookies={"Authorization": f"Bearer {create_access_token}"}
    )

    response = client.delete("/tasks/2/")
    assert response.status_code == 204


def test_delete_record_not_found(
    test_db, create_test_data, create_access_token
):
    client = TestClient(
        app, cookies={"Authorization": f"Bearer {create_access_token}"}
    )
    response = client.delete("/tasks/10/")
    assert response.status_code == 404
    assert response.text == "The resource doesn't exist"
