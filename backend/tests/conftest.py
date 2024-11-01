import pytest
from fastapi.testclient import TestClient
from piccolo.apps.user.tables import BaseUser
from piccolo.table import create_db_tables_sync, drop_db_tables_sync

from apps.tasks.tables import Task
from main import app
from tests.piccolo_conf_test import DB

TABLES = [BaseUser, Task]


@pytest.fixture(autouse=True)
def test_db():
    for _table in TABLES:
        _table._meta._db = DB
    create_db_tables_sync(*TABLES, if_not_exists=True)
    yield
    drop_db_tables_sync(*TABLES)


@pytest.fixture
def create_test_data():
    user = BaseUser(
        username="testuser",
        email="testuser@user.com",
        password="testuser123",
        active=True,
    )
    user.save().run_sync()

    user = BaseUser.select().first().run_sync()

    first_task = Task(
        name="Test task one",
        completed=False,
        task_user=user["id"],
    )

    first_task.save().run_sync()

    second_task = Task(
        name="Test second one",
        completed=True,
        task_user=user["id"],
    )

    second_task.save().run_sync()


@pytest.fixture
def create_access_token() -> str:
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

    access_token = response.json()["access_token"]
    return access_token
