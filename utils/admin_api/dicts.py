from databases.connections import DataBaseConnections
from databases.customer_api import DataBaseCustomerApi
from environment import ENV_OBJECT


class AdminDicts:

    def __init__(self, admin):
        self.admin = admin
        self.db_connections = DataBaseConnections()
        self.db_customer_api = DataBaseCustomerApi()

    def form_connections_delivery_services(self, delivery_service_code: str):
        r"""Форма для снятия с модерации СД.
        :param delivery_service_code: Название СД.
        """
        shop_id = self.db_connections.get_list_shops()[0]
        return {
            "shopId": shop_id,
            "customerId": ENV_OBJECT.customer_id(),
            "connectionId": self.db_customer_api.get_connections_id(shop_id=shop_id)[0],
            "agreementId": "19852a56-8e10-4516-8218-8acefc2c2bd2",
            "customerAgreementId": ENV_OBJECT.customer_agreements_id(),
            "credential": dict(),
            "deliveryService": delivery_service_code
        }

    @staticmethod
    def form_update_connection(settings: dict):
        r"""Форма для обновления connection.
        :param settings: Настройки для разных СД.
        """
        return dict(data=settings)

    @staticmethod
    def form_settings_ds_kaz_post():
        """Фома обновления connection для СД KazPost."""
        return {
            "intakePostOfficeCode": "7777",
            "bin": "123456789012",
            "counterparty": "888.664",
            "acceptanceEmail": "test@mail.ru"
        }

    @staticmethod
    def form_settings_ds_alemtat():
        """Фома обновления connection для СД AlemTat."""
        return {
        "card":"21543134",
        "contract":"14378",
        "receivingStation":"ALA"
    }
