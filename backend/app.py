import typing as t

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from piccolo.engine import engine_finder
from piccolo_admin.endpoints import create_admin
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.csrf.middleware import CSRFMiddleware
from piccolo_api.fastapi.endpoints import FastAPIKwargs, FastAPIWrapper
from starlette.middleware import Middleware
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from accounts.endpoints import oauth2_scheme, router
from home.endpoints import HomeEndpoint
from home.piccolo_app import APP_CONFIG
from home.tables import Task

app = FastAPI(
    routes=[
        Route("/", HomeEndpoint),
        Mount(
            "/admin/",
            create_admin(
                tables=APP_CONFIG.table_classes,
                # Required when running under HTTPS:
                # allowed_hosts=['my_site.com']
            ),
        ),
        Mount("/static/", StaticFiles(directory="static")),
    ],
    middleware=[Middleware(CSRFMiddleware)],
)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


FastAPIWrapper(
    root_url="/tasks/",
    fastapi_app=app,
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


@app.on_event("startup")
async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


@app.on_event("shutdown")
async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")
