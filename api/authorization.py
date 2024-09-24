from api.apiv2_methods.apiv2_dicts.dicts import Dicts
from utils.http_methods import HttpMethod
from utils.environment import ENV_OBJECT
import requests
import time


class ApiAuthorization:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin
        self.session = requests.Session()
        self.response = None

    def post_access_token(self, admin: bool = None, timeout: int = 180, retry_interval: int = 5):
        r"""Метод получения bearer-токена с ожиданием.
        :param admin: Параметр для получения bearer-токена для admin API.
        :param timeout: Максимальное время ожидания в секундах (по умолчанию 2 минуты).
        :param retry_interval: Интервал между повторными попытками в секундах (по умолчанию 5 секунд).
        """
        start_time = time.time()
        last_exception = None
        while time.time() - start_time < timeout:
            try:
                self.response = self.session.post(url=f"{ENV_OBJECT.get_base_url()}/auth/access_token",
                                                  data=Dicts.form_authorization(admin=admin),
                                                  headers=Dicts.form_headers())
                if self.response.status_code == 200:
                    return HttpMethod.return_result(response=self.response)
                else:
                    print(f"Ошибка при получение токена: {self.response.status_code} - {self.response.text}")
            except requests.RequestException as e:
                print(f"Ошибка при получение токена: {e}")

            time.sleep(retry_interval)

        raise AssertionError(f"Не удалось получить токен за {timeout} секунд. "
                             f"Ошибка: статус код {self.response.status_code} - {self.response.text}")
