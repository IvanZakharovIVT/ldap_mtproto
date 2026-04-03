from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.main_app.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        return await self._session.scalar(stmt)

    async def update_user(self, username: str, link: str) -> Optional[User]:
        await self._session.execute(
            update(User).where(User.username == username).values(tg_link=link)
        )
        await self._session.flush()
        await self._session.commit()

    async def create_user(self, username: str, link: str) -> Optional[User]:

        db_obj = User(username=username, tg_link=link)
        self._session.add(db_obj)
        await self._session.flush()
        await self._session.commit()
