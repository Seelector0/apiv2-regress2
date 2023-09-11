from utils.admin_api.connections_delivery_services.connections_delivery_services import ApiModerationDeliveryServices
from utils.http_methods import HttpMethod
from utils.dicts import Dict
import requests


class Admin:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.response = None
        self.http_method = HttpMethod(self, self)
        self.moderation = ApiModerationDeliveryServices(self)
        self.dict = Dict(self, self)

    def admin_session(self):
        """Метод для открытия сессии под admin."""
        data = self.dict.form_authorization(admin=True)
        self.response = self.session.post(url=self.base_url, data=data, headers=self.dict.form_headers())
        return self.http_method.return_result(response=self.response)

    def admin_token(self):
        """Метод получения токена для авторизации в admin api."""
        return self.dict.form_token(authorization=self.response.json()["access_token"])
