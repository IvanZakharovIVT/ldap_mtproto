from fastapi import HTTPException, status


class UserAuthorizationError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, username: str):
        self.username = username

    @property
    def detail(self) -> str:
        return (
            f'Ошибка авторизации для {self.username}. Неверно указан логин или пароль'
        )


class PasswordUpdateError(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, username: str):
        self.username = username

    @property
    def detail(self) -> str:
        return f'Ошибка смены пароля для {self.username}. Указан неверный пароль'
