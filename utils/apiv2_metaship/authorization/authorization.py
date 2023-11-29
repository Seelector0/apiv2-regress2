from environment import ENV_OBJECT
from utils.dicts import Dicts
import requests


class ApiAuthorization:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin
        self.session = requests.Session()

    def post_access_token(self, admin: bool = None):
        r"""Метод получение bearer-токена.
        :param admin: Получение bearer-токена для AdminApi.   
        """
        data = Dicts.form_authorization(admin=admin)
        headers = Dicts.form_headers()
        return self.session.post(url=f"{ENV_OBJECT.get_base_url()}/auth/access_token", data=data, headers=headers)
