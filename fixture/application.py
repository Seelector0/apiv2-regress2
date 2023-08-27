from utils.apiv2_metaship.delivery_serviches.delivery_services import ApiDeliveryServices
from utils.apiv2_metaship.warehouses.warehouses import ApiWarehouse
from utils.apiv2_metaship.documents.documents import ApiDocument
from utils.apiv2_metaship.webhooks.webhooks import ApiWebhook
from utils.apiv2_metaship.intakes.intakes import ApiIntakes
from utils.apiv2_metaship.widgets.widgets import ApiWidget
from utils.apiv2_metaship.parcels.parcels import ApiParcel
from utils.apiv2_metaship.offers.offers import ApiOffers
from utils.apiv2_metaship.orders.orders import ApiOrder
from utils.apiv2_metaship.shops.shops import ApiShop
from utils.apiv2_metaship.info.info import ApiInfo
from utils.http_methods import HttpMethod
from environment import ENV_OBJECT
from utils.dicts import Dict
import requests


class Application:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.response = None
        self.http_method = HttpMethod(self, self)
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
        self.intakes = ApiIntakes(self)
        self.dict = Dict(self, self)

    def open_session(self):
        """Метод для открытия сессии."""
        data = self.dict.form_authorization(client_id=f"{ENV_OBJECT.client_id()}",
                                            client_secret=f"{ENV_OBJECT.client_secret()}")
        self.response = self.session.post(url=self.base_url, data=data, headers=self.dict.form_headers())
        if self.response.status_code == 200:
            return self.response
        else:
            self.session.close()

    def token(self):
        """Метод получения токена для авторизации в apiv2 metaship."""
        return self.dict.form_token(authorization=f"Bearer {self.response.json()['access_token']}")

    def close_session(self):
        """Метод для закрытия сессии."""
        self.session.close()
