from utils.api.delivery_serviches.delivery_services import ApiDeliveryServices
from utils.api.documents.documents import ApiDocument
from utils.api.info.info import ApiInfo
from utils.api.offers.offers import ApiOffers
from utils.api.orders.orders import ApiOrder
from utils.api.parcels.parcels import ApiParcel
from utils.api.warehouses.warehouses import ApiWarehouse
from utils.api.webhooks.webhooks import ApiWebhook
from utils.api.widgets.widgets import ApiWidget
from utils.http_methods import HttpMethod
from utils.api.shops.shops import ApiShop
from environment import ENV_OBJECT
from requests import Response
import requests
import time


class Application:

    def __init__(self, base_url: str = None, response: Response = None, token: dict = None):
        self.base_url = base_url
        self.session = requests.Session()
        self.data = {
            "grant_type": "client_credentials",
            "client_id": f"{ENV_OBJECT.client_id()}",
            "client_secret": f"{ENV_OBJECT.client_secret()}"
        }
        self.response = response
        self.token = token
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.time = time
        self.http_method = HttpMethod(self)
        self.info = ApiInfo(self)
        self.shop = ApiShop(self)
        self.warehouse = ApiWarehouse(self)
        self.service = ApiDeliveryServices(self)
        self.offers = ApiOffers(self)
        self.order = ApiOrder(self)
        self.parcel = ApiParcel(self)
        self.document = ApiDocument(self)
        self.widget = ApiWidget(self)
        self.webhook = ApiWebhook(self)

    def open_session(self):
        """Метод для открытия сессии."""
        self.response = self.session.post(url=self.base_url, data=self.data, headers=self.headers)
        return self.response

    def time_sleep(self, sec: float = 0):
        r"""Метод ожидания в секундах.
        :param sec: Секунды ожидания по умолчанию 0.
        """
        self.time.sleep(sec)

    def close_session(self):
        """Метод для закрытия сессии."""
        self.session.close()
