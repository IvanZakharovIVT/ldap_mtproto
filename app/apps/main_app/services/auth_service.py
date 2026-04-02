from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPBindError

from app.core.config import settings


class AuthService:
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
