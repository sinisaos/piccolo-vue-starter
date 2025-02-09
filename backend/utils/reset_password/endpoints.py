from __future__ import annotations

import base64
import smtplib
import typing as t
from abc import ABCMeta, abstractmethod
from json import JSONDecodeError

from piccolo.apps.user.tables import BaseUser
from starlette.endpoints import HTTPEndpoint, Request
from starlette.exceptions import HTTPException
from starlette.responses import (
    JSONResponse,
)

if t.TYPE_CHECKING:  # pragma: no cover
    from starlette.responses import Response


class ResetPasswordEndpoint(HTTPEndpoint):

    async def post(self, request: Request) -> Response:
        # Some middleware (for example CSRF) has already awaited the request
        # body, and adds it to the request.
        body: t.Any = request.scope.get("form")

        if not body:
            try:
                body = await request.json()
            except JSONDecodeError:
                body = await request.form()

        new_password = body.get("new_password", None)
        confirm_new_password = body.get("confirm_new_password", None)
        token = body.get("token", None)
        min_password_length = 6

        if (not new_password) or (not confirm_new_password):
            error = "Form is invalid. Missing one or more fields."
            raise HTTPException(status_code=422, detail=error)

        if len(new_password) < min_password_length:
            error = (
                f"Password must be at least {min_password_length} characters "
                "long."
            )
            raise HTTPException(
                status_code=422,
                detail=error,
            )

        if confirm_new_password != new_password:
            error = "Passwords do not match."
            raise HTTPException(status_code=422, detail=error)

        # encoding and decoding email
        email_bytes = base64.b64decode(token.encode("ascii"))
        email_string = email_bytes.decode("ascii")

        user = (
            await BaseUser.select(BaseUser.id)
            .where(BaseUser.email == email_string)
            .first()
        )
        if user is not None:
            await BaseUser.update_password(
                user=user["id"], password=new_password
            )

        content = (
            "Password reset was successful. "
            "Please log in again to complete the process."
        )

        return JSONResponse(content=content, status_code=200)


def reset_password() -> t.Type[ResetPasswordEndpoint]:
    """
    An endpoint for reseting passwords.
    """

    class _ResetPasswordEndpoint(ResetPasswordEndpoint):
        pass

    return _ResetPasswordEndpoint


class ForgotPasswordEndpoint(HTTPEndpoint, metaclass=ABCMeta):

    @property
    @abstractmethod
    def _email_host(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def _email_port(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def _email_use_tls(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def _email_host_user(self) -> t.Optional[str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def _email_host_password(self) -> t.Optional[str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def _receiver(self) -> str:
        raise NotImplementedError

    async def post(self, request: Request) -> Response:
        # Some middleware (for example CSRF) has already awaited the request
        # body, and adds it to the request.
        body: t.Any = request.scope.get("form")

        if not body:
            try:
                body = await request.json()
            except JSONDecodeError:
                body = await request.form()

        sender = body.get("email", None)

        # encoding and decoding token
        token_bytes = base64.b64encode(sender.encode("ascii"))
        token_string = token_bytes.decode("ascii")

        if not await BaseUser.exists().where(BaseUser.email == sender):
            error_message = "The user with that email does not exist"
            raise HTTPException(status_code=404, detail=error_message)

        message = f"""
        From: <{self._receiver}>
        To: <{sender}>
        Subject: Reset password

        To initiate the password reset process for account, we send you token:

        Token - {token_string}

        Use this token to set a new password.

        Best regards
        """

        try:
            mail_server = smtplib.SMTP(
                host=self._email_host, port=self._email_port
            )
            if (
                self._email_use_tls
                and self._email_host_user is not None
                and self._email_host_password is not None
            ):
                mail_server.starttls()
                mail_server.login(
                    self._email_host_user, self._email_host_password
                )
            mail_server.sendmail(sender, self._receiver, message)
            content = (
                "We've emailed you token for re-setting your password. "
                "You should receive them shortly. If you don't receive "
                "an email, check your spam folder."
            )

            return JSONResponse(content=content, status_code=200)
        except (smtplib.SMTPException, ConnectionRefusedError):
            error_message = "Unable to send email"
            raise HTTPException(status_code=500, detail=error_message)


def forgot_password(
    email_host: str = "localhost",
    email_port: int = 8025,
    email_use_tls: bool = False,
    email_host_user: t.Optional[str] = None,
    email_host_password: t.Optional[str] = None,
    receiver: str = "info@example.com",
) -> t.Type[ForgotPasswordEndpoint]:
    """
    An endpoint for forgot passwords.

    :param email_host:
        Modify SMTP host. Default to ``localhost``.
    :param email_port:
        Modify SMTP port. Default to ``8025``.
    :param email_use_tls:
        Modify to use Transport Layer Security (TLS).
        Default to ``False``.
    :param email_host_user:
        Modify when use Transport Layer Security (TLS).
    :param email_host_password:
        Modify when use Transport Layer Security (TLS).
    :param receiver:
        Modify to use your email address.
        Default to ``info@example.com``.

    """

    class _ForgotPasswordEndpoint(ForgotPasswordEndpoint):
        _email_host = email_host
        _email_port = email_port
        _email_use_tls = email_use_tls
        _email_host_user = email_host_user
        _email_host_password = email_host_password
        _receiver = receiver

    return _ForgotPasswordEndpoint
