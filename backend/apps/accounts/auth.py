import typing as t

from fastapi import HTTPException, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: t.Optional[str] = None,
        scopes: t.Optional[dict] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": token_url, "scopes": scopes},  # type: ignore
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> t.Optional[str]:
        authorization = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param
