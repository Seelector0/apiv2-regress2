from databases.customer_api import DataBaseCustomerApi
from databases.connections import DataBaseConnections
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())


class ApiConnectionDeliveryServices:

    def __init__(self, admin):
        self.admin = admin
        self.link = "configurations"
        self.db_connections = DataBaseConnections()
        self.db_customer_api = DataBaseCustomerApi()

    def post_connections_russian_post(self):
        """Снятие с модерация СД RussianPost."""
        russian_post = self.admin.dicts.form_connections_delivery_services(delivery_service_code="RussianPost")
        russian_post["credential"]["token"] = os.getenv("RP_TOKEN")
        russian_post["credential"]["secret"] = os.getenv("RP_SECRET")
        result = self.admin.http_method.post(link=self.link, json=russian_post, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_topdelivery(self):
        """Снятие с модерации СД TopDelivery."""
        topdelivery = self.admin.dicts.form_connections_delivery_services(delivery_service_code="TopDelivery")
        topdelivery["credential"]["username"] = os.getenv("TD_USER_NAME")
        topdelivery["credential"]["password"] = os.getenv("TD_PASSWORD")
        topdelivery["credential"]["basicLogin"] = os.getenv("TD_BASIC_LOGIN")
        topdelivery["credential"]["basicPassword"] = os.getenv("TD_BASIC_PASSWORD")
        result = self.admin.http_method.post(link=self.link, json=topdelivery, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_boxberry(self):
        """Снятие с модерации СД Boxberry."""
        boxberry = self.admin.dicts.form_connections_delivery_services(delivery_service_code="Boxberry")
        boxberry["credential"]["token"] = os.getenv("BB_API_TOKEN")
        result = self.admin.http_method.post(link=self.link, json=boxberry, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_cdek(self):
        """Снятие с модерации СД Cdek."""
        cdek = self.admin.dicts.form_connections_delivery_services(delivery_service_code="Cdek")
        cdek["credential"]["account"] = os.getenv("CDEK_ACCOUNT")
        cdek["credential"]["password"] = os.getenv("CDEK_PASSWORD")
        result = self.admin.http_method.post(link=self.link, json=cdek, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_dpd(self):
        """Снятие с модерации СД Dpd."""
        dpd = self.admin.dicts.form_connections_delivery_services(delivery_service_code="Dpd")
        dpd["credential"]["clientNumber"] = os.getenv("DPD_CLIENT_NUMBER")
        dpd["credential"]["clientKey"] = os.getenv("DPD_CLIENT_KEY")
        result = self.admin.http_method.post(link=self.link, json=dpd, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_five_post(self):
        """Снятие с модерации СД FivePost."""
        five_post = self.admin.dicts.form_connections_delivery_services(delivery_service_code="FivePost")
        five_post["credential"]["apiKey"] = os.getenv("FIVE_POST_API_KEY")
        five_post["credential"]["partnerNumber"] = os.getenv("FIVE_POST_PARTNER_NUMBER")
        five_post["credential"]["baseWeight"] = int(os.getenv("FIVE_POST_BASE_WEIGHT"))
        result = self.admin.http_method.post(link=self.link, json=five_post, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_yandex_go(self):
        """Снятие с модерации СД YandexGo."""
        yandex_go = self.admin.dicts.form_connections_delivery_services(delivery_service_code="YandexGo")
        yandex_go["credential"]["yandexGoToken"] = os.getenv("YA_GO_TOKEN")
        yandex_go["credential"]["inn"] = os.getenv("YA_DELIVERY_INN")
        result = self.admin.http_method.post(link=self.link, json=yandex_go, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_yandex_delivery(self):
        """Снятие с модерации СД YandexDelivery."""
        yandex_delivery = self.admin.dicts.form_connections_delivery_services(delivery_service_code="YandexDelivery")
        yandex_delivery["credential"]["yandexDeliveryToken"] = os.getenv("YA_DELIVERY_TOKEN")
        yandex_delivery["credential"]["inn"] = os.getenv("YA_DELIVERY_INN")
        yandex_delivery["credential"]["intakePointCode"] = os.getenv("YA_DELIVERY_INTAKE_POINT_CODE")
        result = self.admin.http_method.post(link=self.link, json=yandex_delivery, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_dalli(self):
        """Снятие с модерации СД Dalli."""
        dalli = self.admin.dicts.form_connections_delivery_services(delivery_service_code="Dalli")
        dalli["credential"]["token"] = os.getenv("DALLI_TOKEN")
        result = self.admin.http_method.post(link=self.link, json=dalli, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_halva(self):
        """Снятие с модерации СД Halva."""
        halva = self.admin.dicts.form_connections_delivery_services(delivery_service_code="Halva")
        halva["credential"]["client"] = os.getenv("HALVA_CLIENT_AND_KEY")
        halva["credential"]["key"] = os.getenv("HALVA_CLIENT_AND_KEY")
        result = self.admin.http_method.post(link=self.link, json=halva, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_kaz_post(self):
        """Снятие с модерации СД KazPost."""
        kaz_post = self.admin.dicts.form_connections_delivery_services(delivery_service_code="KazPost")
        kaz_post["credential"]["key"] = os.getenv("KAZ_POST_KEY")
        result = self.admin.http_method.post(link=self.link, json=kaz_post, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_alemtat(self):
        """Снятие с модерации СД AlemTat."""
        alemtat = self.admin.dicts.form_connections_delivery_services(delivery_service_code="AlemTat")
        alemtat["credential"]["apiKey"] = os.getenv("ALEMTAT_KEY")
        result = self.admin.http_method.post(link=self.link, json=alemtat, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_cse(self):
        """Снятие с модерации СД Cse."""
        cse = self.admin.dicts.form_connections_delivery_services(delivery_service_code="Cse")
        cse["credential"]["login"] = os.getenv("CSE_LOGIN")
        cse["credential"]["password"] = os.getenv("CSE_PASSWORD")
        cse["credential"]["token"] = os.getenv("CSE_TOKEN")
        result = self.admin.http_method.post(link=self.link, json=cse, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_pony_express(self):
        """Снятие с модерации СД PonyExpress."""
        pony_express = self.admin.dicts.form_connections_delivery_services(delivery_service_code="PonyExpress")
        pony_express["credential"]["accessKey"] = os.getenv("PONY_ACCESS_KEY")
        result = self.admin.http_method.post(link=self.link, json=pony_express, admin=True)
        return self.admin.http_method.return_result(response=result)

    def post_connections_metaship(self):
        """Снятие с модерации СД MetaShip."""
        metaship = self.admin.dicts.form_connections_delivery_services(delivery_service_code="MetaShip",
                                                                       index_shop_id=-1)
        metaship["credential"] = list()
        result = self.admin.http_method.post(link=self.link, json=metaship, admin=True)
        return self.admin.http_method.return_result(response=result)

    def put_update_connection_id(self, settings: dict, index_shop_id: int = 0):
        r"""Обновления подключения СД.
        :param settings: Настройки для разных СД.
        :param index_shop_id: Индекс магазина.
        """
        shop_id = self.db_connections.get_list_shops()[index_shop_id]
        connections_id = self.db_customer_api.get_connections_id(shop_id=shop_id)
        put_update = self.admin.dicts.form_update_connection(settings=settings)
        result = self.admin.http_method.put(link=f"connection/{connections_id[-1]}", json=put_update, admin=True)
        return self.admin.http_method.return_result(response=result)
