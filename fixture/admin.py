from utils.admin_api.connections_delivery_services.moderation_delivery_services import ApiModerationDeliveryServices
from dotenv import load_dotenv, find_dotenv
from utils.http_methods import HttpMethod
from utils.dicts import Dict
import requests
import os


load_dotenv(find_dotenv())


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
        data = self.dict.form_authorization(client_id=os.getenv("ADMIN_ID"),
                                            client_secret=os.getenv("ADMIN_SECRET"),
                                            admin=True)
        self.response = self.session.post(url=self.base_url, data=data, headers=self.dict.form_headers())
        if self.response.status_code == 200:
            return self.response
        else:
            self.session.close()

    def admin_token(self):
        """Метод получения токена для авторизации в admin api."""
        return self.dict.form_token(authorization=f"Bearer {self.response.json()['access_token']}")

    def close_session(self):
        """Метод для закрытия сессии."""
        self.session.close()
