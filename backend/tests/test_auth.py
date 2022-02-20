from datetime import datetime
from unittest import TestCase

from fastapi.testclient import TestClient
from piccolo.apps.user.tables import BaseUser
from piccolo.testing.model_builder import ModelBuilder

from app import app
from home.tables import Task


class TestAuth(TestCase):

    token = "fd2ace4d75d53147774fbc8c0cfbd4a2"

    def setUp(self):
        BaseUser.create_table(if_not_exists=True).run_sync()
        Task.create_table(if_not_exists=True).run_sync()
        ModelBuilder.build_sync(BaseUser)
        ModelBuilder.build_sync(Task)

    def tearDown(self):
        Task.alter().drop_table().run_sync()
        BaseUser.alter().drop_table().run_sync()

    def test_auth(self):
        client = TestClient(app)

        # user registration
        payload = {
            "username": "user",
            "email": "user@user.com",
            "password": 1234,
        }

        response = client.post(
            "/accounts/register/",
            json=payload,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "user")

        # user login
        payload = {
            "username": "user",
            "password": 1234,
        }

        response = client.post(
            "/accounts/login/",
            data=payload,
            headers={"content-type": "application/x-www-form-urlencoded"},
        )

        # user profile
        task = (
            Task(
                name="Task 10",
                completed=True,
                created_at=datetime.now(),
                task_user=1,
            )
            .save()
            .run_sync()
        )

        response = client.get(
            "/accounts/profile/tasks/",
            cookies={"Authorization": f"Bearer {response.json()['access_token']}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["task_user"], 1)

        # user logout
        response = client.get(
            "/accounts/logout/",
            cookies={"Authorization": f"Bearer {self.token}"},
        )
        self.assertEqual(response.status_code, 204)

        # user delete
        payload = {
            "username": "user",
            "password": 1234,
        }

        response = client.post(
            "/accounts/login/",
            data=payload,
            headers={"content-type": "application/x-www-form-urlencoded"},
        )

        response_delete = client.get(
            "/accounts/delete/",
            cookies={"Authorization": f"Bearer {response.json()['access_token']}"},
        )
        self.assertEqual(response.status_code, 200)
