import json
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.main_app.repositories.mtproto_repository import MTProtoRepository
from app.apps.main_app.repositories.user_repository import UserRepository
from app.core.config import settings


class MTProtoService:
    def __init__(self, session: AsyncSession):
        self._mtproto_repository = MTProtoRepository(
            settings.MTPROTO_HOST,
            settings.MTPROTO_USERNAME,
            settings.MTPROTO_PASSWORD,
        )
        self._user_repository = UserRepository(session)

    async def generate_new_link(self, username: str) -> str:
        result = self._mtproto_repository.generate_link(username)
        json_result = json.loads(result)
        link = json_result.get('msg', {}).get('link')
        await self._user_repository.update_user(username, link)
        return link

    async def revoke_link(self, username: str):
        self._mtproto_repository.rewoke_link(username)
        await self._user_repository.update_user(username, None)
