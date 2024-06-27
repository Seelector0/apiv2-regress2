from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class SettingsModeration:

    def __init__(self, admin):
        self.admin = admin

    def russian_post(self, shop_id):
        """Модерация СД RussianPost."""
        russian_post = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id,
                                                                           delivery_service_code="RussianPost")
        russian_post["credential"]["token"] = os.getenv("RP_TOKEN")
        russian_post["credential"]["secret"] = os.getenv("RP_SECRET")
        return russian_post

    def topdelivery(self, shop_id):
        """Модерация СД TopDelivery."""
        topdelivery = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id,
                                                                          delivery_service_code="TopDelivery")
        topdelivery["credential"]["username"] = os.getenv("TD_USER_NAME")
        topdelivery["credential"]["password"] = os.getenv("TD_PASSWORD")
        topdelivery["credential"]["basicLogin"] = os.getenv("TD_BASIC_LOGIN")
        topdelivery["credential"]["basicPassword"] = os.getenv("TD_BASIC_PASSWORD")
        return topdelivery

    def boxberry(self, shop_id):
        """Модерация СД Boxberry."""
        boxberry = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id,
                                                                       delivery_service_code="Boxberry")
        boxberry["credential"]["token"] = os.getenv("BB_API_TOKEN")
        return boxberry

    def cdek(self, shop_id):
        """Модерация СД Cdek."""
        cdek = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id, delivery_service_code="Cdek")
        cdek["credential"]["account"] = os.getenv("CDEK_ACCOUNT")
        cdek["credential"]["password"] = os.getenv("CDEK_PASSWORD")
        return cdek

    def dpd(self, shop_id):
        """Модерация СД Dpd."""
        dpd = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id, delivery_service_code="Dpd")
        dpd["credential"]["clientNumber"] = os.getenv("DPD_CLIENT_NUMBER")
        dpd["credential"]["clientKey"] = os.getenv("DPD_CLIENT_KEY")
        return dpd

    def five_post(self, shop_id):
        """Модерация СД FivePost."""
        five_post = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id,
                                                                        delivery_service_code="FivePost")
        five_post["credential"]["apiKey"] = os.getenv("FIVE_POST_API_KEY")
        five_post["credential"]["partnerNumber"] = os.getenv("FIVE_POST_PARTNER_NUMBER")
        five_post["credential"]["baseWeight"] = int(os.getenv("FIVE_POST_BASE_WEIGHT"))
        return five_post

    def yandex_go(self, shop_id):
        """Модерация СД YandexGo."""
        yandex_go = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id,
                                                                        delivery_service_code="YandexGo")
        yandex_go["credential"]["yandexGoToken"] = os.getenv("YA_GO_TOKEN")
        yandex_go["credential"]["inn"] = os.getenv("YA_DELIVERY_INN")
        return yandex_go

    def yandex_delivery(self, shop_id):
        """Модерация СД YandexDelivery."""
        yandex_delivery = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id,
                                                                              delivery_service_code="YandexDelivery")
        yandex_delivery["credential"]["yandexDeliveryToken"] = os.getenv("YA_DELIVERY_TOKEN")
        yandex_delivery["credential"]["inn"] = os.getenv("YA_DELIVERY_INN")
        yandex_delivery["credential"]["intakePointCode"] = os.getenv("YA_DELIVERY_INTAKE_POINT_CODE")
        return yandex_delivery

    def dalli(self, shop_id):
        """Модерация СД Dalli."""
        dalli = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id, delivery_service_code="Dalli")
        dalli["credential"]["token"] = os.getenv("DALLI_TOKEN")
        return dalli

    def halva(self, shop_id):
        """Модерация СД Halva."""
        halva = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id, delivery_service_code="Halva")
        halva["credential"]["client"] = os.getenv("HALVA_CLIENT_AND_KEY")
        halva["credential"]["key"] = os.getenv("HALVA_CLIENT_AND_KEY")
        return halva

    def kaz_post(self, shop_id):
        """Модерация СД KazPost."""
        kaz_post = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id, delivery_service_code="KazPost")
        kaz_post["credential"]["key"] = os.getenv("KAZ_POST_KEY")
        return kaz_post

    def alemtat(self, shop_id):
        """Модерация СД AlemTat."""
        alemtat = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id, delivery_service_code="AlemTat")
        alemtat["credential"]["apiKey"] = os.getenv("ALEMTAT_KEY")
        return alemtat

    def cse(self, shop_id):
        """Модерация СД Cse."""
        cse = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id, delivery_service_code="Cse")
        cse["credential"]["login"] = os.getenv("CSE_LOGIN")
        cse["credential"]["password"] = os.getenv("CSE_PASSWORD")
        cse["credential"]["token"] = os.getenv("CSE_TOKEN")
        return cse

    def pony_express(self, shop_id):
        """Модерация СД PonyExpress."""
        pony_express = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id,
                                                                           delivery_service_code="PonyExpress")
        pony_express["credential"]["accessKey"] = os.getenv("PONY_ACCESS_KEY")
        return pony_express

    def metaship(self, shop_id):
        """Модерация СД MetaShip."""
        metaship = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id,
                                                                       delivery_service_code="MetaShip")
        metaship["credential"] = list()
        return metaship

    def pecom(self, shop_id):
        """Модерации СД Pecom."""
        pecom = self.admin.dicts.form_connections_delivery_services(shop_id=shop_id, delivery_service_code="Pecom")
        pecom["credential"]["login"] = os.getenv("PECOM_LOGIN")
        pecom["credential"]["apiKey"] = os.getenv("PECOM_API_KEY")
        pecom["credential"]["senderWarehouseId"] = os.getenv("PECOM_SENDER_WAREHOUSE_ID")
        return pecom
