from utils.admin_api.connections_delivery_services.moderation_delivery_services import ApiModerationDeliveryServices
from dotenv import load_dotenv, find_dotenv
from utils.http_methods import HttpMethod
from requests import Response
import requests
import allure
import uuid
import os


class Admin:

    load_dotenv(find_dotenv())

    def __init__(self, base_url: str = None, response: Response = None):
        self.base_url = base_url
        self.session = requests.Session()
        self.response = response
        self.http_method = HttpMethod(self)
        self.moderation = ApiModerationDeliveryServices(self)

    def admin_session(self):
        """Метод для открытия сессии."""
        data = {
            "grant_type": "client_credentials",
            "client_id": f"{os.getenv('ADMIN_ID')}",
            "client_secret": f"{os.getenv('ADMIN_SECRET')}",
            "scope": "admin"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.response = self.session.post(url=self.base_url, data=data, headers=headers)
        if self.response.status_code == 200:
            return self.response
        else:
            self.session.close()

    def admin_token(self):
        """Метод получения токена для авторизации в apiv2 metaship."""
        x_trace_id = str(uuid.uuid4())
        with allure.step(title=f"x-trace-id: {x_trace_id}"):
            token = {
                "x-trace-id": x_trace_id,
                "Authorization": f"Bearer {self.response.json()['access_token']}"
            }
            return token

    def close_session(self):
        """Метод для закрытия сессии."""
        self.session.close()
