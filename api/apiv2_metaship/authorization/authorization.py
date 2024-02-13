from utils.http_methods import HttpMethod
from environment import ENV_OBJECT
from api.apiv2_metaship.dicts import Dicts
import requests


class ApiAuthorization:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin
        self.session = requests.Session()
        self.response = None

    def post_access_token(self, admin: bool = None):
        r"""Метод получение bearer-токена.
        :param admin: Параметр для получения bearer-токена для admin api.
        """
        self.response = self.session.post(url=f"{ENV_OBJECT.get_base_url()}/auth/access_token",
                                          data=Dicts.form_authorization(admin=admin), headers=Dicts.form_headers())
        if self.response.status_code >= 500:
            breakpoint()
        return HttpMethod.return_result(response=self.response)
