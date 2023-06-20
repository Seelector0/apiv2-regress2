from environment import ENV_OBJECT
import requests
import allure
import uuid


class HttpMethod:

    def __init__(self, app):
        self.app = app

    def token(self):
        token = {
            "x-trace-id": str(uuid.uuid4()),
            "Authorization": f"Bearer {self.app.response.json()['access_token']}"
        }
        return token

    def get(self, link: str, params=None):
        with allure.step(f"GET requests to URL '{link}'"):
            return self._send(link=link, data=params, headers=self.token(), method='GET')

    def post(self, link: str, data=None, files=None):
        with allure.step(f"POST requests to URL '{link}'"):
            return self._send(link=link, data=data, headers=self.token(), method='POST', files=files)

    def patch(self, link: str, data=None):
        with allure.step(f"POST requests to URL '{link}'"):
            return self._send(link=link, data=data, headers=self.token(), method='PATCH')

    def put(self, link: str, data=None):
        with allure.step(f"PUT requests to URL '{link}'"):
            return self._send(link=link, data=data, headers=self.token(), method='PUT')

    def delete(self, link: str, data=None):
        with allure.step(f"DELETE requests to URL '{link}'"):
            return self._send(link=link, data=data, headers=self.token(), method='DELETE')

    @staticmethod
    def _send(data, headers: dict, method: str, files=None, link: str = None):
        link = f"{ENV_OBJECT.get_base_url()}/v2/{link}"
        if method == 'GET':
            response = requests.get(url=link, params=data, headers=headers)
        elif method == 'POST':
            response = requests.post(url=link, data=data, headers=headers, files=files)
        elif method == 'PATCH':
            response = requests.patch(url=link, data=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(url=link, data=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url=link, data=data, headers=headers)
        else:
            raise Exception(f"Получен неверный HTTP метод '{method}'")
        return response
