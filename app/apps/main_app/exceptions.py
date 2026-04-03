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


class UserDoesntExist(HTTPException):
    """Исключение, выбрасываемое, если в модели отсутствует объект."""

    def __init__(
        self,
        username: str,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пользоватль {username} не найден',
        )



class PasswordUpdateError(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, username: str):
        self.username = username

    @property
    def detail(self) -> str:
        return f'Ошибка смены пароля для {self.username}. Указан неверный пароль'


class MTProtoResponseError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    @property
    def detail(self) -> str:
        return 'Ошибка ответа сервера mtproto'


