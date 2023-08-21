from environment import ENV_OBJECT
import requests
import allure
import json


class HttpMethod:

    def __init__(self, app):
        self.app = app

    @staticmethod
    def url(admin: bool = None):
        r"""Метод для получения url.
        :param admin: Для использования admin url.
        """
        if admin is True:
            url = f"{ENV_OBJECT.get_base_url()}/admin/v2/"
        else:
            url = f"{ENV_OBJECT.get_base_url()}/v2/"
        return url

    def get(self, link: str, params: dict = None, token: dict = None, admin: bool = None):
        r"""GET запрос.
        :param link: Ссылка на запрос.
        :param params: Тело запроса если нужно.
        :param token: Токен для сессии.
        :param admin: Для использования admin URL.
        """
        if token is None:
            token = self.app.token()
        with allure.step(title=f"GET requests to URL '{self.url(admin=admin)}{link}'"):
            result = requests.get(url=f"{self.url(admin=admin)}{link}", params=params, headers=token)
        with allure.step(title=f"Request: {params}"):
            return result

    def post(self, link: str, data: dict = None, files=None, token: dict = None, admin: bool = None):
        r"""POST запрос.
        :param link: Ссылка на запрос.
        :param data: Тело запроса в формате JSON.
        :param files: Передаваемый файл.
        :param token: Токен для сессии.
        :param admin: Для использования admin URL.
        """
        if token is None:
            token = self.app.token()
        with allure.step(title=f"POST requests to URL '{self.url(admin=admin)}{link}'"):
            if files is None:
                result = requests.post(url=f"{self.url(admin=admin)}{link}", data=json.dumps(data), headers=token)
            else:
                result = requests.post(url=f"{self.url()}{link}", data=data, headers=token, files=files)
        with allure.step(title=f"Request: {data}"):
            return result

    def patch(self, link: str, data: dict = None, token: dict = None, admin: bool = None):
        r"""PATCH запрос.
        :param link: Ссылка на запрос.
        :param data: Тело запроса в формате JSON.
        :param token: Токен для сессии.
        :param admin: Для использования admin URL.
        """
        if token is None:
            token = self.app.token()
        with allure.step(title=f"PATCH requests to URL '{self.url(admin=admin)}{link}'"):
            result = requests.patch(url=f"{self.url(admin=admin)}{link}", data=json.dumps(data), headers=token)
        with allure.step(title=f"Request: {data}"):
            return result

    def put(self, link: str, token: dict = None, data: dict = None, admin: bool = None):
        r"""PUT запрос.
        :param link: Ссылка на запрос.
        :param data: Тело запроса в формате JSON.
        :param token: Токен для сессии.
        :param admin: Для использования admin URL.
        """
        if token is None:
            token = self.app.token()
        with allure.step(title=f"PUT requests to URL '{self.url(admin=admin)}{link}'"):
            result = requests.put(url=f"{self.url(admin=admin)}{link}", data=json.dumps(data), headers=token)
        with allure.step(title=f"Request: {data}"):
            return result

    def delete(self, link: str, token: dict = None, admin: bool = None):
        r"""DELETE запрос.
        :param link: Ссылка на запрос.
        :param token: Токен для сессии.
        :param admin: Для использования admin URL.
        """
        if token is None:
            token = self.app.token()
        with allure.step(title=f"DELETE requests to URL '{self.url(admin=admin)}{link}'"):
            return requests.delete(url=f"{self.url(admin=admin)}{link}", headers=token)
