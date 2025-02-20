from typing import Any

from fastapi.security import OAuth2PasswordRequestForm
from piccolo.apps.user.tables import BaseUser

from apps.accounts.schema import UserModelIn, UserModelOut
from apps.tasks.tables import Task


class UserService:
    """
    User service class
    """

    async def user_login(
        self,
        form_data: OAuth2PasswordRequestForm,
    ) -> dict[str, Any] | None:
        user = await BaseUser.login(
            username=form_data.username, password=form_data.password
        )
        return (
            await BaseUser.select()
            .where(BaseUser._meta.primary_key == user)
            .first()
        )

    async def user_register(self, user: UserModelIn) -> UserModelOut:
        payload = user.model_dump()
        if await BaseUser.exists().where(
            BaseUser.email == user.email
        ) or await BaseUser.exists().where(BaseUser.username == user.username):
            raise Exception(
                "User with that email or username already exists.",
            )
        result = BaseUser(**payload)
        await result.save()
        return UserModelOut(**result.to_dict())

    async def delete_user(
        self,
        current_user: UserModelOut,
    ) -> None:
        await BaseUser.delete().where(
            BaseUser._meta.primary_key == current_user.id
        )

    async def user_tasks_list(
        self,
        current_user: UserModelOut,
    ) -> list:
        return (
            await Task.select()
            .where(Task.task_user == current_user.id)
            .order_by(Task._meta.primary_key, ascending=False)
        )


user_service = UserService()
