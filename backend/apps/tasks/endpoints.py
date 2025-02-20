from fastapi import APIRouter, Depends
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.fastapi.endpoints import FastAPIKwargs, FastAPIWrapper

from apps.accounts.utils import oauth2_scheme
from apps.tasks.tables import Task

tasks_router = APIRouter()

FastAPIWrapper(
    root_url="/tasks/",
    fastapi_app=tasks_router,
    piccolo_crud=PiccoloCRUD(
        table=Task,
        read_only=False,
    ),
    fastapi_kwargs=FastAPIKwargs(
        all_routes={"tags": ["Task"]},
        post={"dependencies": [Depends(oauth2_scheme)]},
        put={"dependencies": [Depends(oauth2_scheme)]},
        patch={"dependencies": [Depends(oauth2_scheme)]},
        delete_single={"dependencies": [Depends(oauth2_scheme)]},
    ),
)
