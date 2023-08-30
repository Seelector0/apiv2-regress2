from dotenv import load_dotenv, find_dotenv
from fixture.database import DataBase
from environment import ENV_OBJECT
import os


load_dotenv(find_dotenv())


class ApiDeliveryServices:

    def __init__(self, app):
        self.app = app
        self.database_connections = DataBase(database=ENV_OBJECT.db_connections())

    def link_delivery_services(self):
        """Метод получения ссылки для подключения СД."""
        return f"{self.app.shop.link}/{self.database_connections.metaship.get_list_shops()[0]}/delivery_services"

    def post_delivery_services_russian_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки RussianPost к магазину
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            russian_post = self.app.dict.form_connection_type(delivery_service_code="RussianPost", aggregation=True)
        else:
            russian_post = self.app.dict.form_connection_type(delivery_service_code="RussianPost")
            russian_post["data"]["token"] = os.getenv("RP_TOKEN")
            russian_post["data"]["secret"] = os.getenv("RP_SECRET")
        russian_post["data"]["intakePostOfficeCode"] = "101000"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=russian_post)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_topdelivery(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки TopDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            topdelivery = self.app.dict.form_connection_type(delivery_service_code="TopDelivery", aggregation=True)
        else:
            topdelivery = self.app.dict.form_connection_type(delivery_service_code="TopDelivery")
            topdelivery["data"]["username"] = os.getenv("TD_USER_NAME")
            topdelivery["data"]["password"] = os.getenv("TD_PASSWORD")
            topdelivery["data"]["basicLogin"] = os.getenv("TD_BASIC_LOGIN")
            topdelivery["data"]["basicPassword"] = os.getenv("TD_BASIC_PASSWORD")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=topdelivery)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_boxberry(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Boxberry к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            boxberry = self.app.dict.form_connection_type(delivery_service_code="Boxberry", aggregation=True)
        else:
            boxberry = self.app.dict.form_connection_type(delivery_service_code="Boxberry")
            boxberry["data"]["token"] = os.getenv("BB_API_TOKEN")
        boxberry["data"]["intakeDeliveryPointCode"] = "00127"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=boxberry)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_cdek(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Cdek к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            cdek = self.app.dict.form_connection_type(delivery_service_code="Cdek", aggregation=True)
        else:
            cdek = self.app.dict.form_connection_type(delivery_service_code="Cdek")
            cdek["data"]["account"] = os.getenv("CDEK_ACCOUNT")
            cdek["data"]["password"] = os.getenv("CDEK_PASSWORD")
        cdek["data"]["shipmentPointCode"] = "AKHT1"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=cdek)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_dpd(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Dpd к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            dpd = self.app.dict.form_connection_type(delivery_service_code="Dpd", aggregation=True)
        else:
            dpd = self.app.dict.form_connection_type(delivery_service_code="Dpd")
            dpd["data"]["clientNumber"] = os.getenv("DPD_CLIENT_NUMBER")
            dpd["data"]["clientKey"] = os.getenv("DPD_CLIENT_KEY")
        dpd["data"]["intakePointCode"] = "M16"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dpd)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_cse(self):
        """Настройки подключения службы доставки Cse к магазину."""
        cse = self.app.dict.form_connection_type(delivery_service_code="Cse")
        cse["data"]["login"] = os.getenv("CSE_LOGIN")
        cse["data"]["password"] = os.getenv("CSE_PASSWORD")
        cse["data"]["token"] = os.getenv("CSE_TOKEN")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=cse)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_five_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки FivePost к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            five_post = self.app.dict.form_connection_type(delivery_service_code="FivePost", aggregation=True)
        else:
            five_post = self.app.dict.form_connection_type(delivery_service_code="FivePost")
            five_post["data"]["apiKey"] = os.getenv("FIVE_POST_API_KEY")
            five_post["data"]["partnerNumber"] = os.getenv("FIVE_POST_PARTNER_NUMBER")
            five_post["data"]["baseWeight"] = int(os.getenv("FIVE_POST_BASE_WEIGHT"))
        result = self.app.http_method.post(link=self.link_delivery_services(), json=five_post)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_svyaznoy(self):
        """Настройки подключения службы доставки Svyaznoy к магазину."""
        svyaznoy = self.app.dict.form_connection_type(delivery_service_code="Svyaznoy")
        svyaznoy["data"]["login"] = os.getenv("SL_LOGIN")
        svyaznoy["data"]["password"] = os.getenv("SL_PASSWORD")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=svyaznoy)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_yandex_go(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки YandexGo к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            yandex_go = self.app.dict.form_connection_type(delivery_service_code="YandexGo", aggregation=True)
        else:
            yandex_go = self.app.dict.form_connection_type(delivery_service_code="YandexGo")
            yandex_go["data"]["token"] = os.getenv("YA_GO_TOKEN")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=yandex_go)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_yandex_delivery(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки YandexDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            yandex_delivery = self.app.dict.form_connection_type(delivery_service_code="YandexDelivery",
                                                                 aggregation=True)
        else:
            yandex_delivery = self.app.dict.form_connection_type(delivery_service_code="YandexDelivery")
            yandex_delivery["data"]["token"] = os.getenv("YA_DELIVERY_TOKEN")
            yandex_delivery["data"]["inn"] = os.getenv("YA_DELIVERY_INN")
            yandex_delivery["data"]["intakePointCode"] = os.getenv("YA_DELIVERY_INTAKE_POINT_CODE")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=yandex_delivery)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_dostavka_club(self):
        """Настройки подключения службы доставки DostavkaClub к магазину."""
        dostavka_club = self.app.dict.form_connection_type(delivery_service_code="DostavkaClub")
        dostavka_club["data"]["login"] = os.getenv("CLUB_LOGIN")
        dostavka_club["data"]["pass"] = os.getenv("CLUB_PASSWORD")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dostavka_club)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_dostavka_guru(self):
        """Настройки подключения службы доставки DostavkaGuru к магазину."""
        dostavka_guru = self.app.dict.form_connection_type(delivery_service_code="DostavkaGuru")
        dostavka_guru["data"]["partnerId"] = int(os.getenv("GURU_PARTNER_ID"))
        dostavka_guru["data"]["key"] = os.getenv("GURU_KEY")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dostavka_guru)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_l_post(self):
        """Настройки подключения службы доставки LPost к магазину."""
        l_post = self.app.dict.form_connection_type(delivery_service_code="LPost")
        l_post["data"]["secret"] = os.getenv("L_POST_SECRET")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=l_post)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_dalli(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Dalli к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            dalli = self.app.dict.form_connection_type(delivery_service_code="Dalli", aggregation=True)
        else:
            dalli = self.app.dict.form_connection_type(delivery_service_code="Dalli")
            dalli["data"]["token"] = os.getenv("DALLI_TOKEN")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dalli)
        return self.app.http_method.return_result(response=result)

    def get_delivery_services(self):
        """Метод получения списка выполненных настроек СД к магазину."""
        result = self.app.http_method.get(link=self.link_delivery_services())
        return self.app.http_method.return_result(response=result)

    def get_delivery_services_code(self, code: str):
        r"""Получение настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        result = self.app.http_method.get(link=f"{self.link_delivery_services()}/{code}")
        return self.app.http_method.return_result(response=result)

    def patch_delivery_services_tariffs(self, code: str, tariffs):
        r"""Метод редактирования тарифов СД.
        :param code: Код СД.
        :param tariffs: Тарифы СД.
        """
        patch = self.app.dict.form_patch_body(op="replace", path="settings.tariffs", value={
            "exclude": tariffs,
            "restrict": None
            })
        result = self.app.http_method.patch(link=f"{self.link_delivery_services()}/{code}", json=patch)
        return self.app.http_method.return_result(response=result)

    def patch_delivery_services(self, code: str, value: bool = True):
        r"""Метод редактирования полей настройки подключения к СД.
        :param code: Код СД.
        :param value: Скрытие СД из ЛК при False.
        """
        patch = self.app.dict.form_patch_body(op="replace", path="visibility", value=value)
        result = self.app.http_method.patch(link=f"{self.link_delivery_services()}/{code}", json=patch)
        return self.app.http_method.return_result(response=result)

    def post_activate_delivery_service(self, code: str):
        r"""Активация настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        return self.app.http_method.post(link=f"{self.link_delivery_services()}/{code}/activate")

    def post_deactivate_delivery_service(self, code: str):
        r"""Деактивация настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        return self.app.http_method.post(link=f"{self.link_delivery_services()}/{code}/deactivate")
