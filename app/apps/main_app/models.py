from sqlalchemy import Column, String

from app.core.models import BaseDBModel


class User(BaseDBModel):
    """Схема БД для пользователей."""

    __tablename__ = 'users'

    username = Column(String(100), unique=True, nullable=False, primary_key=True)
    tg_link = Column(String(255), nullable=True)
