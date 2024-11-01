import typing as t

from piccolo.apps.user.tables import BaseUser
from piccolo_api.crud.serializers import create_pydantic_model
from pydantic import BaseModel


# token schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: t.Optional[str] = None


# user schema
UserModelInBase: t.Any = create_pydantic_model(
    table=BaseUser,
    exclude_columns=(
        BaseUser.active,
        BaseUser.admin,
        BaseUser.superuser,
    ),
    model_name="UserModelIn",
)
UserModelOutBase: t.Any = create_pydantic_model(
    table=BaseUser,
    include_default_columns=True,
    model_name="UserModelOut",
)


# keep Pylance happy
class UserModelIn(UserModelInBase): ...


class UserModelOut(UserModelOutBase): ...
