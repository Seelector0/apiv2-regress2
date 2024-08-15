from api.apiv2_methods.apiv2_dicts.dicts import Dicts
from utils.http_methods import HttpMethod
from utils.environment import ENV_OBJECT
import requests

class ApiAuthorization:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin
        self.session = requests.Session()
        self.response = None

    def post_access_token(self, admin: bool = None):
        r"""Метод получения bearer-токена.
        :param admin: Параметр для получения bearer-токена для admin API.
        """
        try:
            self.response = self.session.post(url=f"{ENV_OBJECT.get_base_url()}/auth/access_token",
                                              data=Dicts.form_authorization(admin=admin), headers=Dicts.form_headers())
            if self.response.status_code >= 400:
                raise AssertionError(f"Ошибка при получение токена: {self.response.status_code} - {self.response.text}")

            return HttpMethod.return_result(response=self.response)
        except requests.RequestException as e:
            raise AssertionError(f"Ошибка при получение токена: {e}")

