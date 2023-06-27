from environment import ENV_OBJECT
import requests
import allure
import uuid


class HttpMethod:

    def __init__(self, app):
        self.app = app

    def token(self):
        """Метод получения токена для авторизации."""
        x_trace_id = str(uuid.uuid4())
        with allure.step(f"x-trace-id: {x_trace_id}"):
            token = {
                "x-trace-id": x_trace_id,
                "Authorization": f"Bearer {self.app.response.json()['access_token']}"
            }
            return token

    def get(self, link: str, params=None):
        r"""GET запрос.
        :param link: Ссылка на запрос.
        :param params: Тело запроса если нужно.
        """
        with allure.step(f"GET requests to URL '{ENV_OBJECT.get_base_url()}/v2/{link}'"):
            link = f"{ENV_OBJECT.get_base_url()}/v2/{link}"
            return requests.get(url=link, params=params, headers=self.token())

    def post(self, link: str, data=None, files=None):
        r"""POST запрос.
        :param link: Ссылка на запрос.
        :param data: Тело запроса в формате JSON.
        :param files: Передаваемый файл.
        :return:
        """
        with allure.step(f"POST requests to URL '{ENV_OBJECT.get_base_url()}/v2/{link}'"):
            link = f"{ENV_OBJECT.get_base_url()}/v2/{link}"
            return requests.post(url=link, data=data, headers=self.token(), files=files)

    def patch(self, link: str, data=None):
        r"""PATCH запрос.
        :param link: Ссылка на запрос.
        :param data: Тело запроса в формате JSON.
        """
        with allure.step(f"PATCH requests to URL '{ENV_OBJECT.get_base_url()}/v2/{link}'"):
            link = f"{ENV_OBJECT.get_base_url()}/v2/{link}"
            return requests.patch(url=link, data=data, headers=self.token())

    def put(self, link: str, data=None):
        r"""PUT запрос.
        :param link: Ссылка на запрос.
        :param data: Тело запроса в формате JSON.
        """
        with allure.step(f"PUT requests to URL '{ENV_OBJECT.get_base_url()}/v2/{link}'"):
            link = f"{ENV_OBJECT.get_base_url()}/v2/{link}"
            return requests.put(url=link, data=data, headers=self.token())

    def delete(self, link: str):
        r"""DELETE запрос.
        :param link: Ссылка на запрос.
        """
        with allure.step(f"DELETE requests to URL '{ENV_OBJECT.get_base_url()}/v2/{link}'"):
            link = f"{ENV_OBJECT.get_base_url()}/v2/{link}"
            return requests.delete(url=link, headers=self.token())
