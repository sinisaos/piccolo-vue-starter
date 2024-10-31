import typing as t
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from piccolo.apps.user.tables import BaseUser

from apps.accounts.auth import OAuth2PasswordBearerCookie
from apps.accounts.schema import TokenData, UserModelIn, UserModelOut
from apps.tasks.tables import Task
from config.base import settings

oauth2_scheme = OAuth2PasswordBearerCookie(token_url="accounts/login")
router = APIRouter(prefix="/accounts")


def create_access_token(
    data: dict,
    expires_delta: t.Optional[timedelta] = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = (
        await BaseUser.select()
        .where(BaseUser.username == token_data.username)
        .first()
        .run()
    )
    if user is None:
        raise credentials_exception
    return user


@router.post("/login/", tags=["Auth"])
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await BaseUser.login(
        username=form_data.username, password=form_data.password
    )
    result = await BaseUser.select().where(BaseUser.id == user).first().run()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": result["username"]}, expires_delta=access_token_expires  # type: ignore
    )
    token = jsonable_encoder(access_token)
    response = JSONResponse(
        {
            "access_token": access_token,
            "token_type": "bearer",
        }
    )
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",  # type: ignore
        secure=True,
    )

    return response


@router.post("/register/", response_model=UserModelOut, tags=["Auth"])
async def register_user(user: UserModelIn):
    payload = user.model_dump()
    if (
        await BaseUser.exists().where(BaseUser.email == user.email).run()
        or await BaseUser.exists()
        .where(BaseUser.username == user.username)
        .run()
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with that email or username already exists.",
        )
    result = BaseUser(**payload)
    await result.save().run()
    return UserModelOut(**user.__dict__)


@router.get("/profile/", response_model=UserModelOut, tags=["User profile"])
async def user_profile(
    current_user: UserModelOut = Depends(get_current_user),
):
    return current_user


@router.get("/profile/tasks/", tags=["User profile"])
async def user_tasks(
    current_user: UserModelOut = Depends(get_current_user),
):
    tasks = (
        await Task.select()
        .where(Task.task_user == current_user["id"])
        .order_by(Task._meta.primary_key, ascending=False)
        .run()
    )
    return tasks


@router.delete("/delete/", response_model=UserModelOut, tags=["User profile"])
async def user_delete(
    current_user: UserModelOut = Depends(get_current_user),
):
    await BaseUser.delete().where(
        BaseUser._meta.primary_key == current_user["id"]
    ).run()

    return Response(status_code=204)


@router.get("/logout/", tags=["Auth"])
def logout(request: Request):
    response = Response(status_code=204)
    response.delete_cookie("Authorization")
    return response
