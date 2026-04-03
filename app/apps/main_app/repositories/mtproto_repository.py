import paramiko

from app.apps.main_app.exceptions import MTProtoResponseError


class MTProtoRepository:
    def __init__(self, host: str, username: str, password: str):
        self._host = host
        self._username = username
        self._password = password

    @staticmethod
    def __init_connection() -> paramiko.SSHClient:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return client

    async def __run_command(self, command: str):
        client = self.__init_connection()
        try:
            client.connect(
                hostname=self._host,
                username=self._username,
                password=self._password,
            )

            stdin, stdout, stderr = client.exec_command(command)

            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if output:
                result = output
            else:
                raise MTProtoResponseError
            if error:
                print("=== Ошибка ===")
                print(error)

        except paramiko.AuthenticationException:
            print("Ошибка: Неверное имя пользователя или пароль.")
        except paramiko.SSHException as e:
            print(f"Ошибка SSH: {e}")
        except Exception as e:
            print(f"Общая ошибка: {e}")
        finally:
            client.close()

    async def generate_link(self, username: str):
        return self.__run_command(command = f"bash MTProtoProxyInstall.sh 4 {username}")

    async def rewoke_link(self, username: str):
        return self.__run_command(command=f"bash MTProtoProxyInstall.sh 5 {username}")
