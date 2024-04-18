from databases.connections import DataBaseConnections
from databases.customer_api import DataBaseCustomerApi
from dotenv import load_dotenv, find_dotenv
from utils.environment import ENV_OBJECT
import os


load_dotenv(find_dotenv())


class AdminDicts:

    def __init__(self, admin):
        self.admin = admin
        self.db_connections = DataBaseConnections()
        self.db_customer_api = DataBaseCustomerApi()

    def form_connections_delivery_services(self, delivery_service_code: str, index_shop_id=0):
        r"""Форма для снятия с модерации СД.
        :param delivery_service_code: Название СД.
        :param index_shop_id: Индекс магазина.
        """
        shop_id = self.db_connections.get_list_shops()[index_shop_id]
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
        """Фоhма обновления подключения для СД KazPost."""
        return {
            "intakePostOfficeCode": os.getenv("KAZ_POST_INTAKE_POST_OFFICE_CODE"),
            "bin": os.getenv("KAZ_POST_BIN"),
            "counterparty": os.getenv("KAZ_POST_COUNTERPARTY"),
            "acceptanceEmail": os.getenv("KAZ_POST_ACCEPTANCE_EMAIL")
        }

    @staticmethod
    def form_settings_ds_alemtat():
        """Фома обновления подключения для СД AlemTat."""
        return {
            "card": os.getenv("ALEMTAT_CARD"),
            "contract": os.getenv("ALEMTAT_CONTRACT"),
            "receivingStation": os.getenv("ALEMTAT_RECEIVING_STATION")
        }

    @staticmethod
    def form_settings_ds_boxberry():
        return dict(intakeDeliveryPointCode=os.getenv("BB_INTAKE_DELIVERY_POINT_CODE"))

    def form_settings_ds_metaship(self):
        return {
            "data": [
                {
                    "deliveryService": "Boxberry",
                    "tariff": "_default",
                    "shopId": self.db_connections.get_list_shops()[0]
                }
            ]
        }
