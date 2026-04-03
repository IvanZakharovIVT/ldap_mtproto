from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPBindError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.main_app.exceptions import UserAuthorizationError
from app.apps.main_app.repositories.ldap_repository import LDAPRepository
from app.apps.main_app.repositories.user_repository import UserRepository
from app.core.config import settings


class LDAPService:
    def __init__(self, session: AsyncSession):
        self._ldap_repository = LDAPRepository()
        self._user_repository = UserRepository(session)

    async def is_user_exist(self, username: str, password: str) -> bool:
        server = Server(settings.LDAP_HOST, get_info=ALL)
        try:
            conn = Connection(server, user=username, password=password, auto_bind=True)
            result = conn.bound
            conn.unbind()
            return result
        except LDAPBindError as e:
            print(e)
            return False

    async def get_user(self, username: str, password: str):
        if not await self._ldap_repository.is_user_exist(username, password):
            raise UserAuthorizationError(username)
        user = await self._user_repository.get_by_username(username)
        if not user:
            await self._user_repository.create_user(username=username, link='')
            user = await self._user_repository.get_by_username(username)
        return user
