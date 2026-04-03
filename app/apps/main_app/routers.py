from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.main_app.exceptions import UserAuthorizationError
from app.apps.main_app.schemas import UserAuthSchemaBase
from app.apps.main_app.security import get_data_from_access_token
from app.apps.main_app.services.auth_service import LDAPService
from app.apps.main_app.utils import set_auth_token, delete_cookie
from app.core.config import settings
from app.core.database import get_session

router = APIRouter(tags=['router'])


@router.post(
    '/user/auth',
    summary='Авторизация в системе',
    description='Токены сохраняются в cookie',
    response_model=dict,
)
async def auth_cookie(
    response: Response,
    credentials_schema: UserAuthSchemaBase,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict:
    ldap_service = LDAPService(session)
    if await ldap_service.is_user_exist(credentials_schema.username, credentials_schema.password):
        subject = {
            'username': credentials_schema.username,
        }
        set_auth_token(subject, response)
        response.raw_headers = [
            (item[0], item[1] + b';Partitioned') for item in response.headers.raw
        ]
        return {'message': 'Successfully logged in'}
    raise UserAuthorizationError(credentials_schema.username)


@router.post(
    '/user/logout',
    summary='Выход из системы',
    description='Удаление токенов из cookie',
)
async def logout(
    response: Response,
    current_user: Annotated[dict, Depends(get_data_from_access_token)],
):
    delete_cookie(response, settings.AUTH_TOKEN_NAME)
    return {'message': 'Successfully logout'}


@router.get(
    '/user/check_auth/',
    summary='Проверка авторизованости пользователя',
    description='Проверка авторизованости пользователя. Нужна при переходе на каждую страницу.',
    status_code=status.HTTP_200_OK,
    response_model=bool,
)
async def check_auth(
    current_user: Annotated[dict, Depends(get_data_from_access_token)],
):
    """Проверка авторизованости текущего пользователя"""
    return True
