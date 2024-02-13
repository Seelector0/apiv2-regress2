from api.admin_api.connections_delivery_services.connections_delivery_services import ApiConnectionDeliveryServices
from api.apiv2_metaship.authorization.authorization import ApiAuthorization
from api.admin_api.dicts import AdminDicts
from utils.http_methods import HttpMethod


class Admin:

    def __init__(self):
        self.http_method = HttpMethod(admin=self, app=self)
        self.dicts = AdminDicts(admin=self)
        self.authorization = ApiAuthorization(admin=self, app=self)
        self.moderation = ApiConnectionDeliveryServices(admin=self)
