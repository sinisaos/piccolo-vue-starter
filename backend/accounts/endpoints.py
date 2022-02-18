import typing as t
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from piccolo.apps.user.tables import BaseUser

from accounts.auth import OAuth2PasswordBearerCookie
from accounts.schema import Token, TokenData, UserModelIn, UserModelOut
from home.tables import Task
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearerCookie(token_url="accounts/login")
router = APIRouter(prefix="/accounts")


def create_access_token(
    data: dict, expires_delta: t.Optional[timedelta] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
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

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": result["username"]}, expires_delta=access_token_expires
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
        samesite="Lax",
        secure=True,
    )

    return response


@router.post("/register/", response_model=UserModelOut, tags=["Auth"])
async def register_user(user: UserModelIn):
    user = BaseUser(**user.__dict__)
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
    await user.save().run()
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
        .order_by(Task.id, ascending=False)
        .run()
    )
    return tasks


@router.delete("/delete/", response_model=UserModelOut, tags=["User profile"])
async def user_delete(
    current_user: UserModelOut = Depends(get_current_user),
):
    user = (
        await BaseUser.delete()
        .where(BaseUser._meta.primary_key == current_user["id"])
        .run()
    )
    return Response(status_code=204)


@router.get("/logout", tags=["Auth"])
def logout(request: Request):
    response = Response(status_code=204)
    response.delete_cookie("Authorization")
    return response
