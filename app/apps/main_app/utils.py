from datetime import timedelta

from fastapi import Response

from app.apps.main_app.security import access_security, refresh_security
from app.core.config import settings


def set_token(
    token: str,
    token_name: str,
    max_age: int,
    response: Response,
):
    response.delete_cookie(token_name)
    response.set_cookie(
        key=token_name,
        value=token,
        max_age=max_age,
        samesite='lax',
    )


def set_auth_token(
    subject: dict,
    response: Response,
):
    max_age = settings.AUTH_TOKEN_TIMEDELTA
    auth_token = access_security.create_access_token(
        subject=subject, expires_delta=timedelta(seconds=max_age)
    )
    set_token(auth_token, settings.AUTH_TOKEN_NAME, max_age, response)

def delete_cookie(response: Response, cookie_name: str):
    response.delete_cookie(
        cookie_name,
        httponly=True,
    )
