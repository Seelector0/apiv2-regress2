from api.apiv2_methods.apiv2_dicts.dicts import Dicts
from utils.http_methods import HttpMethod
from utils.environment import ENV_OBJECT
import requests
import logging
import time


class ApiAuthorization:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        self.response = None

    def post_access_token(self, admin: bool = None, timeout: int = 360, retry_interval: int = 5):
        r"""Метод получения bearer-токена с ожиданием.
        :param admin: Параметр для получения bearer-токена для admin API.
        :param timeout: Максимальное время ожидания в секундах (по умолчанию 4 минуты).
        :param retry_interval: Интервал между повторными попытками в секундах (по умолчанию 5 секунд).
        """
        server_error_codes = [502, 503, 504]  # Список кодов ошибок сервера
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                self.response = self.session.post(url=f"{ENV_OBJECT.get_base_url()}/auth/access_token",
                                                  data=Dicts.form_authorization(admin=admin),
                                                  headers=Dicts.form_headers())
                elapsed_time = time.time() - start_time

                if self.response.status_code in server_error_codes:
                    self.logger.warning(
                        f"Ошибка при запросе POST к URL: {self.response.url}. Статус-код {self.response.status_code}. "
                        f"Затраченное время: {elapsed_time:.2f} секунд. Повторная попытка через {retry_interval} секунд.")
                else:
                    return HttpMethod.return_result(response=self.response)

            except requests.RequestException as e:
                elapsed_time = time.time() - start_time
                self.logger.error(
                    f"Ошибка при запросе токена: {e}. Затраченное время: {elapsed_time:.2f} секунд.")

            time.sleep(retry_interval)

        raise AssertionError(f"Не удалось получить токен за {timeout} секунд. "
                             f"Ошибка: статус код {self.response.status_code} - {self.response.text}")
