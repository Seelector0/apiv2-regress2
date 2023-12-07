from utils.admin_api.connections_delivery_services.connections_delivery_services import ApiConnectionDeliveryServices
from utils.apiv2_metaship.authorization.authorization import ApiAuthorization
from utils.admin_api.dicts import AdminDicts
from utils.http_methods import HttpMethod


class Admin:

    def __init__(self):
        self.http_method = HttpMethod(self, self)
        self.dicts = AdminDicts(self)
        self.authorization = ApiAuthorization(self, self)
        self.connections = ApiConnectionDeliveryServices(self)
