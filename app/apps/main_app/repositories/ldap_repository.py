from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import LDAPBindError

from app.apps.main_app.schemas import UserSchema
from app.core.config import settings


class LDAPRepository:
    def __init__(self):
        self._server = Server(settings.LDAP_HOST, get_info=ALL)

    async def get_user(self, username: str, password: str) -> UserSchema:
        conn = None
        try:
            conn = Connection(self._server, user=username, password=password, auto_bind=True)
            conn.search(settings.BASE_ON, f'(uid="{username}")', attributes=['tg_link'])
            return UserSchema(username=username, tg_link=conn.entries[0].tg_link)
        except LDAPBindError as e:
            print(e)
            raise e
        finally:
            if conn:
                conn.unbind()
