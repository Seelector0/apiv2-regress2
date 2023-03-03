from utils.api.delivery_serviches.delivery_services import ApiDeliveryServices
from utils.api.documents.documents import ApiDocument
from utils.logger import Logger
from utils.api.info.info import ApiInfo
from utils.api.offers.offers import ApiOffers
from utils.api.orders.orders import ApiOrder
from utils.api.parcels.parcels import ApiParcel
from utils.api.warehouses.warehouses import ApiWarehouse
from utils.api.webhooks.webhooks import ApiWebhook
from utils.api.widgets.widgets import ApiWidget
from utils.http_methods import HttpMethod
from utils.api.shops.shops import ApiShop
from pathlib import Path
import requests
import os


class Application:

    def __init__(self, base_url=None, response=None, token=None):
        self.logs_directory = str(Path(Path.home(), "PycharmProjects", "Apiv2-regress-version2", "logs"))
        self.base_url = base_url
        self.session = requests.Session()
        self.response = response
        self.token = token
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.http_method = HttpMethod(self)
        self.logger = Logger(self)
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

    def open_session(self, data, headers: dict):
        """Метод для открытия сессии"""
        self.response = self.session.post(url=self.base_url, data=data, headers=headers)
        return self.response

    def clearing_directory(self):
        """Метод для чистки директории с логами"""
        for file in os.listdir(self.logs_directory):
            os.remove(os.path.join(self.logs_directory, file))

    def close_session(self):
        """Метод для закрытия сессии"""
        self.session.close()
