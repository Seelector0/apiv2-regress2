from api.apiv2_metaship.delivery_services import ApiDeliveryServices
from api.apiv2_metaship.apiv2_dicts.dicts import Dicts
from api.apiv2_metaship.warehouses import ApiWarehouse
from api.apiv2_metaship.documents import ApiDocument
from api.apiv2_metaship.webhooks import ApiWebhook
from api.apiv2_metaship.intakes import ApiIntakes
from api.apiv2_metaship.reports import ApiReports
from api.apiv2_metaship.widgets import ApiWidget
from api.apiv2_metaship.parcels import ApiParcel
from api.apiv2_metaship.offers import ApiOffers
from api.authorization import ApiAuthorization
from api.apiv2_metaship.orders import ApiOrder
from api.apiv2_metaship.shops import ApiShop
from api.apiv2_metaship.info import ApiInfo
from api.apiv2_metaship.forms import Forms
from utils.http_methods import HttpMethod


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
