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
import requests


class Application:

    def __init__(self, base_url=None, response=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.response = response
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
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

    def open_session(self, data, headers: dict):
        """Функция для открытия сессии"""
        self.response = self.session.post(url=self.base_url, data=data, headers=headers)
        return self.response

    def close_session(self):
        """Функция для закрытия сессии"""
        self.session.close()
