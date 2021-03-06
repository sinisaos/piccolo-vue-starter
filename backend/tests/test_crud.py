from unittest import TestCase

from fastapi.testclient import TestClient
from piccolo.apps.user.tables import BaseUser
from piccolo.testing.model_builder import ModelBuilder

from app import app
from home.tables import Task


class TestCrud(TestCase):

    token = "fd2ace4d75d53147774fbc8c0cfbd4a2"

    def setUp(self):
        BaseUser.create_table(if_not_exists=True).run_sync()
        Task.create_table(if_not_exists=True).run_sync()
        ModelBuilder.build_sync(BaseUser)
        ModelBuilder.build_sync(Task)

    def tearDown(self):
        Task.alter().drop_table().run_sync()
        BaseUser.alter().drop_table().run_sync()

    def test_get_tasks(self):
        client = TestClient(app)

        response = client.get("/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_get_single_tasks(self):
        client = TestClient(app)

        task = Task.select().first().run_sync()

        response = client.get(f"/tasks/{task['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], task["id"])

    def test_get_tasks_count(self):
        client = TestClient(app)

        response = client.get("/tasks/count/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_task_crud(self):
        client = TestClient(app)

        user = BaseUser.select().first().run_sync()

        payload = {
            "name": "Task 100",
            "completed": False,
            "created_at": "2022-02-20T07:14:27",
            "task_user": user["id"],
        }

        response = client.post(
            "/tasks/",
            json=payload,
            cookies={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), [{"id": 1}])

        payload = {
            "name": "Task 1001",
            "completed": True,
            "created_at": "2022-02-20T07:14:27",
            "task_user": user["id"],
        }

        response = client.patch(
            "/tasks/1/",
            json=payload,
            cookies={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "name": "Task 1001",
                "completed": True,
                "created_at": "2022-02-20T07:14:27",
                "task_user": user["id"],
            },
        )

        response = client.delete(
            "/tasks/1/",
            json=payload,
            cookies={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 204)
