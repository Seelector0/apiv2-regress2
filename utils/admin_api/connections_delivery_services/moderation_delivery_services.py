from dotenv import load_dotenv, find_dotenv
from fixture.database import DataBase
from environment import ENV_OBJECT
import allure
import os


class ApiModerationDeliveryServices:

    load_dotenv(find_dotenv())

    def __init__(self, admin):
        self.admin = admin
        self.database_connections = DataBase(database=ENV_OBJECT.db_connections())
        self.database_customer = DataBase(database=ENV_OBJECT.db_customer_api())
        self.link = "configurations"

    def moderation(self, delivery_service_code):
        r"""Метод снятия СД с модерации.
        :param delivery_service_code: Название СД.
        """
        shop_id = self.database_connections.metaship.get_list_shops()[0]
        connection = {
            "shopId": f"{shop_id}",
            "customerId": f"{ENV_OBJECT.customer_id()}",
            "connectionId": f"{self.database_customer.customer.get_connections_id(shop_id=shop_id)[0]}",
            "agreementId": "19852a56-8e10-4516-8218-8acefc2c2bd2",
            "customerAgreementId": f"{ENV_OBJECT.customer_agreements_id()}",
            "credential": {
            },
            "deliveryService": delivery_service_code
        }
        return connection

    def moderation_russian_post(self):
        """Снятие с модерация СД RussianPost."""
        russian_post = self.moderation(delivery_service_code="RussianPost")
        russian_post["credential"]["token"] = f"{os.getenv('RP_TOKEN')}"
        russian_post["credential"]["secret"] = f"{os.getenv('RP_SECRET')}"
        result = self.admin.http_method.post(link=self.link, data=russian_post, admin=True,
                                             token=self.admin.admin_token())
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def moderation_topdelivery(self):
        """Снятие с модерации СД TopDelivery."""
        topdelivery = self.moderation(delivery_service_code="TopDelivery")
        topdelivery["credential"]["username"] = f"{os.getenv('TD_USER_NAME')}"
        topdelivery["credential"]["password"] = f"{os.getenv('TD_PASSWORD')}"
        topdelivery["credential"]["basicLogin"] = f"{os.getenv('TD_BASIC_LOGIN')}"
        topdelivery["credential"]["basicPassword"] = f"{os.getenv('TD_BASIC_PASSWORD')}"
        result = self.admin.http_method.post(link=self.link, data=topdelivery, admin=True,
                                             token=self.admin.admin_token())
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def moderation_boxberry(self):
        """Снятие с модерации СД Boxberry."""
        boxberry = self.moderation(delivery_service_code="Boxberry")
        boxberry["credential"]["token"] = f"{os.getenv('BB_API_TOKEN')}"
        result = self.admin.http_method.post(link=self.link, data=boxberry, admin=True,
                                             token=self.admin.admin_token())
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def moderation_cdek(self):
        """Снятие с модерации СД Cdek."""
        cdek = self.moderation(delivery_service_code="Cdek")
        cdek["credential"]["account"] = f"{os.getenv('CDEK_ACCOUNT')}"
        cdek["credential"]["password"] = f"{os.getenv('CDEK_PASSWORD')}"
        result = self.admin.http_method.post(link=self.link, data=cdek, admin=True, token=self.admin.admin_token())
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def moderation_dpd(self):
        """Снятие с модерации СД Dpd."""
        dpd = self.moderation(delivery_service_code="Dpd")
        dpd["credential"]["clientNumber"] = f"{os.getenv('DPD_CLIENT_NUMBER')}"
        dpd["credential"]["clientKey"] = f"{os.getenv('DPD_CLIENT_KEY')}"
        result = self.admin.http_method.post(link=self.link, data=dpd, admin=True, token=self.admin.admin_token())
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def moderation_five_post(self):
        """Снятие с модерации СД FivePost"""
        five_post = self.moderation(delivery_service_code="FivePost")
        five_post["credential"]["apiKey"] = f"{os.getenv('FIVE_POST_API_KEY')}"
        five_post["credential"]["partnerNumber"] = f"{os.getenv('FIVE_POST_PARTNER_NUMBER')}"
        five_post["credential"]["baseWeight"] = 1000
        result = self.admin.http_method.post(link=self.link, data=five_post, admin=True,
                                             token=self.admin.admin_token())
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def moderation_yandex_go(self):
        """Снятие с модерации СД YandexGo"""
        yandex_go = self.moderation(delivery_service_code="YandexGo")
        yandex_go["credential"]["yandexGoToken"] = f"{os.getenv('YANDEX_TOKEN')}"
        yandex_go["credential"]["inn"] = "7734381257"
        result = self.admin.http_method.post(link=self.link, data=yandex_go, admin=True,
                                             token=self.admin.admin_token())
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def moderation_dalli(self):
        """Снятие с модерации СД Dalli"""
        dalli = self.moderation(delivery_service_code="Dalli")
        dalli["data"]["token"] = f"{os.getenv('DALLI_TOKEN')}"
        result = self.admin.http_method.post(link=self.link, data=dalli, admin=True, token=self.admin.admin_token())
        with allure.step(title=f"Response: {result.json()}"):
            return result
