from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.security import OAuth2PasswordRequestForm

from apps.accounts.schema import UserModelIn, UserModelOut
from apps.accounts.services import user_service
from apps.accounts.utils import create_access_token, get_current_user
from config.base import settings

auth_router = APIRouter(prefix="/accounts")


@auth_router.post("/login/", tags=["Auth"])
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> JSONResponse:
    user = await user_service.user_login(form_data=form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes
    )
    access_token = await create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires  # type: ignore
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


@auth_router.post("/register/", tags=["Auth"])
async def register_user(user: UserModelIn) -> UserModelOut:
    try:
        return await user_service.user_register(user=user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@auth_router.get("/profile/", tags=["User profile"])
async def user_profile(
    current_user: UserModelOut = Depends(get_current_user),
) -> UserModelOut:
    return current_user


@auth_router.get("/profile/tasks/", tags=["User profile"])
async def user_tasks(
    current_user: UserModelOut = Depends(get_current_user),
) -> list:
    return await user_service.user_tasks_list(current_user=current_user)


@auth_router.delete(
    "/delete/", response_model=UserModelOut, tags=["User profile"]
)
async def user_delete(
    current_user: UserModelOut = Depends(get_current_user),
) -> Response:
    await user_service.delete_user(current_user=current_user)
    return Response(status_code=204)


@auth_router.get("/logout/", tags=["Auth"])
def logout(request: Request) -> Response:
    response = Response(status_code=204)
    response.delete_cookie("Authorization")
    return response
