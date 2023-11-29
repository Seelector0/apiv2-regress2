from utils.admin_api.connections_delivery_services.connections_delivery_services import ApiModerationDeliveryServices
from utils.apiv2_metaship.authorization.authorization import Authorization
from utils.http_methods import HttpMethod
from utils.dicts import Dicts


class Admin:

    def __init__(self):
        self.response = None
        self.http_method = HttpMethod(self, self)
        self.authorization = Authorization(self, self)
        self.moderation = ApiModerationDeliveryServices(self)
        self.dicts = Dicts(self, self)

    def admin_session(self):
        """Метод для открытия сессии под admin."""
        self.response = self.authorization.post_access_token(admin=True)
        return self.http_method.return_result(response=self.response)

    def admin_token(self):
        """Метод получения токена для авторизации в admin api."""
        return self.dicts.form_token(authorization=self.response.json()["access_token"])
