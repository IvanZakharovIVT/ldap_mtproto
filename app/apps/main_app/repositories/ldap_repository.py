from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPBindError

from app.apps.main_app.exceptions import UserAuthorizationError
from app.core.config import settings


class LDAPRepository:
    def __init__(self):
        self._server = Server(settings.LDAP_HOST, get_info=ALL)

    def is_user_exist(self, username: str, password: str) -> bool:
        conn = None
        try:
            conn = Connection(self._server, user=f'uid={username},{settings.BIND_ON}', password=password, auto_bind=True)
            conn.search(settings.BASE_ON, f'(uid={username})')
            if conn.entries:
                return True
            return False
        except LDAPBindError as e:
            print(e)
            raise UserAuthorizationError(username)
        finally:
            if conn:
                conn.unbind()
