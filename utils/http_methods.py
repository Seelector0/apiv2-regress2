from api.apiv2_methods.apiv2_dicts.dicts import Dicts
from utils.environment import ENV_OBJECT
import simplejson.errors
import requests
import logging
import allure
import time


class HttpMethod:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin
        self.logger = logging.getLogger(__name__)
        self.dependent_services = [
            "http://develop.address-service.metaship.ppdev.ru/health/check",
            "http://deliverypoint-api.metaship.ppdev.ru/health/check",
            "https://develop.customer-api.metaship.ppdev.ru/health/check",
        ]

    def get(self, link: str, params: dict = None, admin: bool = None, **kwargs):
        r"""GET запрос.
        :param link: Ссылка на запрос.
        :param params: Тело запроса если нужно.
        :param admin: Для использования admin URL.
        """
        return self._send(method="GET", url=link, params=params, admin=admin, **kwargs)

    def post(self, link: str, json: dict = None, data: dict = None, admin: bool = None, **kwargs):
        r"""POST запрос.
        :param link: Ссылка на запрос.
        :param json: Тело запроса в формате JSON.
        :param data: Тело в формате dict.
        :param admin: Для использования admin URL.
        """
        return self._send(method="POST", url=link, json=json, data=data, admin=admin, **kwargs)

    def patch(self, link: str, admin: bool = None, **kwargs):
        r"""PATCH запрос.
        :param link: Ссылка на запрос.
        :param admin: Для использования admin URL.
        """
        return self._send(method="PATCH", url=link, admin=admin, **kwargs)

    def put(self, link: str, admin: bool = None, **kwargs):
        r"""PUT запрос.
        :param link: Ссылка на запрос.
        :param admin: Для использования admin URL.
        """
        return self._send(method="PUT", url=link, admin=admin, **kwargs)

    def delete(self, link: str, admin: bool = None, **kwargs):
        r"""DELETE запрос.
        :param link: Ссылка на запрос.
        :param admin: Для использования admin URL.
        """
        return self._send(method="DELETE", url=link, admin=admin, **kwargs)

    def _check_dependent_services(self, timeout=120, interval=5):
        """Метод проверяет доступность зависимых сервисов."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            all_services_healthy = True
            for service in self.dependent_services:
                try:
                    response = requests.get(service, timeout=10)
                    if response.status_code != 200:
                        all_services_healthy = False
                        self.logger.error(f"Сервис {service} недоступен, статус: {response.status_code}")
                except requests.RequestException as e:
                    all_services_healthy = False
                    self.logger.error(f"Ошибка при проверке {service}: {e}")

            if all_services_healthy:
                self.logger.info("Все зависимые сервисы доступны.")
                return True

            self.logger.info("Ожидание восстановления зависимых сервисов...")
            time.sleep(interval)

        raise AssertionError("Не удалось дождаться доступности зависимых сервисов за отведенное время.")

    def _send(self, method: str, url: str, params: dict = None, json: dict = None, data: dict = None,
              admin: bool = None, timeout: int = 300, retry_interval: int = 5, headers: dict = None, retries_500=0,
              max_retries_on_500: int = 1, **kwargs):
        r"""Метод для определения запросов с повторной попыткой при ошибках и логированием в Allure.
        :param method: Метод запроса.
        :param url: URL запроса.
        :param params: Параметры запроса для метода GET.
        :param json: Тело запроса в формате JSON.
        :param data: Тело запроса в формате dict.
        :param admin: Для использования admin URL.
        :param timeout: Максимальное время ожидания в секундах.
        :param retry_interval: Интервал между попытками.
        :param headers: Пользовательские заголовки для запроса.
        """
        start_time = time.time()
        server_error_codes = {502, 503, 504}

        if admin:
            token = Dicts.form_token(authorization=self.admin.authorization.response.json()["access_token"])
            url = f"{ENV_OBJECT.get_base_url()}/admin/v2/{url}"
        else:
            token = Dicts.form_token(authorization=self.app.authorization.response.json()["access_token"])
            url = f"{ENV_OBJECT.get_base_url()}/v2/{url}"

        if headers:
            token.update(headers)

        while time.time() - start_time < timeout:
            try:
                with allure.step(title=f"{method} request to URL: {url}"):
                    if method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                        response = requests.request(method=method, url=url, params=params, json=json, data=data,
                                                    headers=token, **kwargs)
                    else:
                        raise Exception(f"Получен неверный HTTP метод '{method}'")
                if params:
                    with allure.step(title=f"""Request: {str(params).replace("'", '"')}"""):
                        pass
                elif data:
                    with allure.step(title=f"""Request: {str(data).replace("'", '"')}"""):
                        pass
                else:
                    with allure.step(title=f"""Request: {str(json).replace("'", '"')}"""):
                        pass

                elapsed_time = time.time() - start_time

                if ENV_OBJECT.db_connections() == "connections":
                    if response.status_code == 500:
                        retries_500 += 1
                        self.logger.warning(f"Получен статус 500 при запросе {method} к {url}. "
                                            f"Проверяем зависимые сервисы...")
                        self._check_dependent_services()
                        if retries_500 > max_retries_on_500:
                            return response
                        self.logger.info("Зависимые сервисы восстановлены. Повтор запроса...")
                        continue

                if response.status_code in server_error_codes:
                    self.logger.error(
                        f"Ошибка при запросе {method} to URL: {url}. Статус-код {response.status_code}. "
                        f"Затраченное время:: {elapsed_time:.2f} секунд.")
                else:
                    return response

            except requests.RequestException as e:
                elapsed_time = time.time() - start_time
                self.logger.error(
                    f"Ошибка при запросе {method} to URL: {url}. {e}. Затраченное время: {elapsed_time:.2f} секунд.")

            time.sleep(retry_interval)

        raise AssertionError(f"Не удалось выполнить {method} запрос на {url} за {timeout} секунд. "
                             f"Статус код {response.status_code}")

    @staticmethod
    def return_result(response):
        r"""Метод возвращает результат ответа.
        :param response: Результат ответа.
        """
        try:
            if response.status_code != 204:
                with allure.step(title=f"""Response: {str(response.json()).replace("'", '"')}"""):
                    return response
            else:
                return response
        except (simplejson.errors.JSONDecodeError, requests.exceptions.JSONDecodeError):
            trace_id = response.request.headers.get('x-trace-id', 'No x-trace-id')
            raise AssertionError(
                f"Ошибка API метода\nКод статуса ответа: {response.status_code}\nx-trace-id: {trace_id}"
            )
