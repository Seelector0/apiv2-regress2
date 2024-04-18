from api.admin_methods.connections_delivery_services import ApiConnectionDeliveryServices
from api.admin_methods.moderation_settings.moderation_settings import SettingsModeration
from api.admin_methods.admin_dicts.dicts import AdminDicts
from api.authorization import ApiAuthorization
from utils.http_methods import HttpMethod


class Admin:

    def __init__(self):
        self.http_method = HttpMethod(admin=self, app=self)
        self.dicts = AdminDicts(admin=self)
        self.authorization = ApiAuthorization(admin=self, app=self)
        self.connection = ApiConnectionDeliveryServices(admin=self)
        self.moderation = SettingsModeration(admin=self)
