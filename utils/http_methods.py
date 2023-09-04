from environment import ENV_OBJECT
import simplejson.errors
import requests
import allure


class HttpMethod:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin

    @staticmethod
    def url(admin: bool = None):
        r"""Метод для получения url.
        :param admin: Для использования admin url.
        """
        if admin is True:
            url = f"{ENV_OBJECT.get_base_url()}/admin/v2"
        else:
            url = f"{ENV_OBJECT.get_base_url()}/v2"
        return url

    def get(self, link: str, params: dict = None, admin: bool = None):
        r"""GET запрос.
        :param link: Ссылка на запрос.
        :param params: Тело запроса если нужно.
        :param admin: Для использования admin URL.
        """
        return self._send(method="GET", url=link, params=params, admin=admin)

    def post(self, link: str, json: dict = None, data: dict = None, files: list = None, admin: bool = None):
        r"""POST запрос.
        :param link: Ссылка на запрос.
        :param json: Тело запроса в формате JSON.
        :param data: Тело в формате dict.
        :param files: Передаваемый файл.
        :param admin: Для использования admin URL.
        """
        return self._send(method="POST", url=link, json=json, data=data, files=files, admin=admin)

    def patch(self, link: str, json: dict, admin: bool = None):
        r"""PATCH запрос.
        :param link: Ссылка на запрос.
        :param json: Тело запроса в формате JSON.
        :param admin: Для использования admin URL.
        """
        return self._send(method="PATCH", url=link, json=json, admin=admin)

    def put(self, link: str, json: dict = None, admin: bool = None):
        r"""PUT запрос.
        :param link: Ссылка на запрос.
        :param json: Тело запроса в формате JSON.
        :param admin: Для использования admin URL.
        """
        return self._send(method="PUT", url=link, json=json, admin=admin)

    def delete(self, link: str, admin: bool = None):
        r"""DELETE запрос.
        :param link: Ссылка на запрос.
        :param admin: Для использования admin URL.
        """
        return self._send(method="DELETE", url=link, admin=admin)

    def _send(self, method: str, url: str, params: dict = None, json: dict = None, data: dict = None,
              files: list = None, admin: bool = None):
        r"""Метод для определения запросов.
        :param method: Метод запроса.
        :param url: URL запроса.
        :param params: Параметр запроса для метода GET.
        :param json: Тело запроса в формате json.
        :param data: Тело запроса в формате data.
        :param files: Передаваемый файл
        :param admin: Для использования admin URL.
        """
        url = f"{self.url(admin=admin)}/{url}"
        if admin is True:
            token = self.admin.admin_token()
        else:
            token = self.app.token()
        with allure.step(title=f"{method} requests tu URL: {url}"):
            if method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                response = requests.request(method=method, url=url, params=params, json=json, data=data, files=files,
                                            headers=token)
            else:
                raise Exception(f"Получен неверный HTTP метод '{method}'")
        if params:
            with allure.step(title=f"Request: {params}"):
                pass
        elif data:
            with allure.step(title=f"Request: {data}"):
                pass
        else:
            with allure.step(title=f"Request: {json}"):
                pass
        return response

    @staticmethod
    def return_result(response):
        r"""Метод возвращает результат запроса.
        :param response: Результат запроса.
        """
        response = response
        try:
            with allure.step(title=f"Response: {response.json()}"):
                return response
        except simplejson.errors.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {response.status_code}")
        except requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {response.status_code}")
