from api.apiv2_methods.settings_delivery_services.settings_delivery_services import SettingsDeliveryServices
from api.apiv2_methods.delivery_services import ApiDeliveryServices
from api.apiv2_methods.apiv2_dicts.dicts import Dicts
from api.apiv2_methods.warehouses import ApiWarehouse
from api.apiv2_methods.documents import ApiDocument
from api.apiv2_methods.webhooks import ApiWebhook
from api.apiv2_methods.intakes import ApiIntakes
from api.apiv2_methods.reports import ApiReports
from api.apiv2_methods.widgets import ApiWidget
from api.apiv2_methods.parcels import ApiParcel
from api.apiv2_methods.offers import ApiOffers
from api.authorization import ApiAuthorization
from api.apiv2_methods.orders import ApiOrder
from api.apiv2_methods.shops import ApiShop
from api.apiv2_methods.info import ApiInfo
from api.apiv2_methods.forms import Forms
from utils.common_tests import CommonInfo
from utils.helper.test_shops import TestsShop
from utils.helper.test_warehouses import TestsWarehouse
from utils.helper.test_webhook import TestsWebHook
from utils.helper.test_widget_api import TestsWidget
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
        self.settings = SettingsDeliveryServices(app=self)
        self.tests_shop = TestsShop(app=self)
        self.tests_warehouse = TestsWarehouse(app=self)
        self.tests_webhook = TestsWebHook(app=self)
        self.tests_info = CommonInfo(app=self)
        self.tests_widget = TestsWidget(app=self)
