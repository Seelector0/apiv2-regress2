from environment import ENV_OBJECT
from utils.dicts import Dicts
import requests


class ApiAuthorization:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin
        self.session = requests.Session()

    def post_access_token(self, admin: bool = None):
        data = Dicts.form_authorization(admin=admin)
        return self.session.post(url=f"{ENV_OBJECT.get_base_url()}/auth/access_token", data=data,
                                 headers=Dicts.form_headers())
