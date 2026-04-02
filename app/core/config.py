from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from pydantic import model_validator
from pydantic_settings import BaseSettings

from app.core.exeptions import MissingEnvVar


class Settings(BaseSettings):
    # COMMON CONFIG
    TITLE: str = 'None-Titled'
    DEBUG: bool = True
    ALLOWED_HOSTS: list[str] = ['*']
    LOG_LEVEL: str = 'INFO'
    TIMEZONE: str = 'UTC'

    # API VERSION CONFIG
    API_V1: str = '/v1'

    # JWT TOKEN
    TOKEN_SECURE: bool = False
    JWT_SECRET_KEY: str
    AUTH_TOKEN_TIMEDELTA: int = 24 * 60 * 60  # 1 день
    AUTH_TOKEN_NAME: str = 'access_token'
    COOKIE_DOMAIN: str | None = None

    LDAP_HOST: str = 'ldap://ldap-test.nordclan:389'
    BASE_ON: str = 'dc=company'

    @model_validator(mode='before')
    @classmethod
    def validate_and_set_defaults(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        for field_name, field in cls.model_fields.items():
            value = data.get(field_name)

            if field.is_required():
                if not value or (isinstance(value, str) and value.strip() == ''):
                    raise MissingEnvVar(
                        f"Поле '{field_name}' обязательно в .env и не может быть пустым"
                    )

            if value is None or (isinstance(value, str) and value.strip() == ''):
                if not field.is_required():
                    data[field_name] = field.default

        return data

    class Config:
        env_file = '.env'
        env_parse_protocol = 'plain'


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
