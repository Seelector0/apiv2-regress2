from apiv2_metaship.dicts import Dicts
from environment import ENV_OBJECT
import simplejson.errors
import requests
import allure


class HttpMethod:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin

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

    def _send(self, method: str, url: str, params: dict = None, json: dict = None, data: dict = None,
              admin: bool = None, **kwargs):
        r"""Метод для определения запросов.
        :param method: Метод запроса.
        :param url: URL запроса.
        :param params: Параметр запроса для метода GET.
        :param json: Тело запроса в формате json.
        :param data: Тело запроса в формате data.
        :param files: Передаваемый файл
        :param admin: Для использования admin URL.
        """
        if admin:
            token = Dicts.form_token(authorization=self.admin.authorization.response.json()["access_token"])
            url = f"{ENV_OBJECT.get_base_url()}/admin/v2/{url}"
        else:
            token = Dicts.form_token(authorization=self.app.authorization.response.json()["access_token"])
            url = f"{ENV_OBJECT.get_base_url()}/v2/{url}"
        with allure.step(title=f"{method} request to URL: {url}"):
            if method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                response = requests.request(method=method, url=url, params=params, json=json, data=data, headers=token,
                                            **kwargs)
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
        return response

    @staticmethod
    def return_result(response):
        r"""Метод возвращает результат ответа.
        :param response: Результат ответа.
        """
        try:
            with allure.step(title=f"""Response: {str(response.json()).replace("'", '"')}"""):
                return response
        except simplejson.errors.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {response.status_code}")
        except requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {response.status_code}")
