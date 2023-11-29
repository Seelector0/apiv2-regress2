from utils.apiv2_metaship.delivery_serviches.delivery_services import ApiDeliveryServices
from utils.apiv2_metaship.authorization.authorization import ApiAuthorization
from utils.apiv2_metaship.warehouses.warehouses import ApiWarehouse
from utils.apiv2_metaship.documents.documents import ApiDocument
from utils.apiv2_metaship.webhooks.webhooks import ApiWebhook
from utils.apiv2_metaship.reports.reports import ApiReports
from utils.apiv2_metaship.intakes.intakes import ApiIntakes
from utils.apiv2_metaship.widgets.widgets import ApiWidget
from utils.apiv2_metaship.parcels.parcels import ApiParcel
from utils.apiv2_metaship.offers.offers import ApiOffers
from utils.apiv2_metaship.orders.orders import ApiOrder
from utils.apiv2_metaship.shops.shops import ApiShop
from utils.apiv2_metaship.info.info import ApiInfo
from utils.apiv2_metaship.forms.forms import Forms
from utils.http_methods import HttpMethod
from utils.dicts import Dicts
import sys


class Application:

    def __init__(self):
        self.response = None
        self.http_method = HttpMethod(self, self)
        self.authorization = ApiAuthorization(self, self)
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
        self.reports = ApiReports(self)
        self.forms = Forms(self)
        self.dicts = Dicts(self, self)

    def open_session(self):
        """Метод для открытия сессии."""
        self.response = self.authorization.post_access_token()
        return self.http_method.return_result(response=self.response)

    def token(self):
        """Метод получения токена для авторизации в apiv2 metaship."""
        return self.dicts.form_token(authorization=self.response.json()["access_token"])
