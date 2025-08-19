from dotenv import load_dotenv, find_dotenv
from utils.environment import ENV_OBJECT
import os

load_dotenv(find_dotenv())


class AdminDicts:

    def __init__(self, admin, customer_api):
        self.admin = admin
        self.customer_api = customer_api

    def form_connections_delivery_services(self, shop_id, delivery_service_code: str):
        r"""Форма для снятия с модерации СД.
        :param delivery_service_code: Название СД.
        :param shop_id: Id магазина.
        """
        return {
            "shopId": shop_id,
            "customerId": ENV_OBJECT.customer_id(),
            "connectionId": self.customer_api.get_connections_id(shop_id=shop_id,
                                                                 delivery_service=delivery_service_code),
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
        """Форма обновления подключения для СД KazPost."""
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
    def form_settings_ds_pecom():
        """Фома обновления подключения для СД AlemTat."""
        return {
            "senderWarehouseId": os.getenv("PECOM_SENDER_WAREHOUSE_ID"),
        }

    @staticmethod
    def form_settings_ds_boxberry():
        return dict(intakeDeliveryPointCode=os.getenv("BB_INTAKE_DELIVERY_POINT_CODE"))

    @staticmethod
    def form_settings_ds_metaship(shop_id):
        return {
            "data": [
                {
                    "deliveryService": "Boxberry",
                    "shopId": shop_id
                }
            ],
            "deliveryPointMapping": [
                {
                    "deliveryService": "Boxberry",
                    "tariff": "_default",
                    "gridCode": None
                }
            ]
        }
