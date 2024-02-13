from apiv2_metaship.delivery_serviches.delivery_services import ApiDeliveryServices
from apiv2_metaship.authorization.authorization import ApiAuthorization
from apiv2_metaship.warehouses.warehouses import ApiWarehouse
from apiv2_metaship.documents.documents import ApiDocument
from apiv2_metaship.webhooks.webhooks import ApiWebhook
from apiv2_metaship.intakes.intakes import ApiIntakes
from apiv2_metaship.reports.reports import ApiReports
from apiv2_metaship.widgets.widgets import ApiWidget
from apiv2_metaship.parcels.parcels import ApiParcel
from apiv2_metaship.offers.offers import ApiOffers
from apiv2_metaship.orders.orders import ApiOrder
from apiv2_metaship.shops.shops import ApiShop
from apiv2_metaship.info.info import ApiInfo
from apiv2_metaship.forms.forms import Forms
from utils.http_methods import HttpMethod
from apiv2_metaship.dicts import Dicts


class Application:

    def __init__(self):
        self.http_method = HttpMethod(app=self, admin=self)
        self.dicts = Dicts(app=self)
        self.authorization = ApiAuthorization(app=self, admin=self)
        self.shop = ApiShop(app=self)
        self.warehouse = ApiWarehouse(app=self)
        self.service = ApiDeliveryServices(app=self)
        self.offers = ApiOffers(app=self)
        self.order = ApiOrder(app=self)
        self.parcel = ApiParcel(app=self)
        self.document = ApiDocument(app=self)
        self.info = ApiInfo(app=self)
        self.intakes = ApiIntakes(app=self)
        self.widget = ApiWidget(app=self)
        self.webhook = ApiWebhook(app=self)
        self.reports = ApiReports(app=self)
        self.forms = Forms(app=self)
