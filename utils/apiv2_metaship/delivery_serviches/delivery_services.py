from databases.connections import DataBaseConnections
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())


class ApiDeliveryServices:

    def __init__(self, app):
        self.app = app
        self.db_connections = DataBaseConnections()

    def link_delivery_services(self):
        """Метод получения ссылки для подключения СД."""
        return f"{self.app.shop.link}/{self.db_connections.get_list_shops()[0]}/delivery_services"

    def post_delivery_services_russian_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки RussianPost к магазину
        :param aggregation: Тип подключения СД по агрегации.
        """
        russian_post = self.app.dicts.form_connection_type(delivery_service_code="RussianPost")
        russian_post["data"]["token"] = os.getenv("RP_TOKEN")
        russian_post["data"]["secret"] = os.getenv("RP_SECRET")
        if aggregation:
            russian_post = self.app.dicts.form_connection_type(delivery_service_code="RussianPost", aggregation=True)
        russian_post["data"]["intakePostOfficeCode"] = "101000"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=russian_post)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_topdelivery(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки TopDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        topdelivery = self.app.dicts.form_connection_type(delivery_service_code="TopDelivery")
        topdelivery["data"]["username"] = os.getenv("TD_USER_NAME")
        topdelivery["data"]["password"] = os.getenv("TD_PASSWORD")
        topdelivery["data"]["basicLogin"] = os.getenv("TD_BASIC_LOGIN")
        topdelivery["data"]["basicPassword"] = os.getenv("TD_BASIC_PASSWORD")
        if aggregation:
            topdelivery = self.app.dicts.form_connection_type(delivery_service_code="TopDelivery", aggregation=True)
        result = self.app.http_method.post(link=self.link_delivery_services(), json=topdelivery)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_boxberry(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Boxberry к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        boxberry = self.app.dicts.form_connection_type(delivery_service_code="Boxberry")
        boxberry["data"]["token"] = os.getenv("BB_API_TOKEN")
        if aggregation:
            boxberry = self.app.dicts.form_connection_type(delivery_service_code="Boxberry", aggregation=True)
        boxberry["data"]["intakeDeliveryPointCode"] = "00127"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=boxberry)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_cdek(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Cdek к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        cdek = self.app.dicts.form_connection_type(delivery_service_code="Cdek")
        cdek["data"]["account"] = os.getenv("CDEK_ACCOUNT")
        cdek["data"]["password"] = os.getenv("CDEK_PASSWORD")
        if aggregation:
            cdek = self.app.dicts.form_connection_type(delivery_service_code="Cdek", aggregation=True)
        cdek["data"]["shipmentPointCode"] = "AKHT1"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=cdek)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_dpd(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Dpd к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        dpd = self.app.dicts.form_connection_type(delivery_service_code="Dpd")
        dpd["data"]["clientNumber"] = os.getenv("DPD_CLIENT_NUMBER")
        dpd["data"]["clientKey"] = os.getenv("DPD_CLIENT_KEY")
        if aggregation:
            dpd = self.app.dicts.form_connection_type(delivery_service_code="Dpd", aggregation=True)
        dpd["data"]["intakePointCode"] = "M16"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dpd)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_cse(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Cse к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        cse = self.app.dicts.form_connection_type(delivery_service_code="Cse")
        cse["data"]["login"] = os.getenv("CSE_LOGIN")
        cse["data"]["password"] = os.getenv("CSE_PASSWORD")
        cse["data"]["token"] = os.getenv("CSE_TOKEN")
        if aggregation:
            cse = self.app.dicts.form_connection_type(delivery_service_code="Cse", aggregation=True)
        result = self.app.http_method.post(link=self.link_delivery_services(), json=cse)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_five_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки FivePost к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        five_post = self.app.dicts.form_connection_type(delivery_service_code="FivePost")
        five_post["data"]["apiKey"] = os.getenv("FIVE_POST_API_KEY")
        five_post["data"]["partnerNumber"] = os.getenv("FIVE_POST_PARTNER_NUMBER")
        five_post["data"]["baseWeight"] = int(os.getenv("FIVE_POST_BASE_WEIGHT"))
        if aggregation:
            five_post = self.app.dicts.form_connection_type(delivery_service_code="FivePost", aggregation=True)
        result = self.app.http_method.post(link=self.link_delivery_services(), json=five_post)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_yandex_go(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки YandexGo к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        yandex_go = self.app.dicts.form_connection_type(delivery_service_code="YandexGo")
        yandex_go["data"]["token"] = os.getenv("YA_GO_TOKEN")
        if aggregation:
            yandex_go = self.app.dicts.form_connection_type(delivery_service_code="YandexGo", aggregation=True)
        result = self.app.http_method.post(link=self.link_delivery_services(), json=yandex_go)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_yandex_delivery(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки YandexDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        yandex_delivery = self.app.dicts.form_connection_type(delivery_service_code="YandexDelivery")
        yandex_delivery["data"]["token"] = os.getenv("YA_DELIVERY_TOKEN")
        yandex_delivery["data"]["inn"] = os.getenv("YA_DELIVERY_INN")
        yandex_delivery["data"]["intakePointCode"] = os.getenv("YA_DELIVERY_INTAKE_POINT_CODE")
        if aggregation:
            yandex_delivery = self.app.dicts.form_connection_type(delivery_service_code="YandexDelivery",
                                                                  aggregation=True)
        result = self.app.http_method.post(link=self.link_delivery_services(), json=yandex_delivery)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_dostavka_club(self):
        """Настройки подключения службы доставки DostavkaClub к магазину."""
        dostavka_club = self.app.dicts.form_connection_type(delivery_service_code="DostavkaClub")
        dostavka_club["data"]["login"] = os.getenv("CLUB_LOGIN")
        dostavka_club["data"]["pass"] = os.getenv("CLUB_PASSWORD")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dostavka_club)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_dostavka_guru(self):
        """Настройки подключения службы доставки DostavkaGuru к магазину."""
        dostavka_guru = self.app.dicts.form_connection_type(delivery_service_code="DostavkaGuru")
        dostavka_guru["data"]["partnerId"] = int(os.getenv("GURU_PARTNER_ID"))
        dostavka_guru["data"]["key"] = os.getenv("GURU_KEY")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dostavka_guru)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_l_post(self):
        """Настройки подключения службы доставки LPost к магазину по интеграции."""
        l_post = self.app.dicts.form_connection_type(delivery_service_code="LPost")
        l_post["data"]["secret"] = os.getenv("L_POST_SECRET")
        result = self.app.http_method.post(link=self.link_delivery_services(), json=l_post)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_dalli(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Dalli к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        dalli = self.app.dicts.form_connection_type(delivery_service_code="Dalli")
        dalli["data"]["token"] = os.getenv("DALLI_TOKEN")
        if aggregation:
            dalli = self.app.dicts.form_connection_type(delivery_service_code="Dalli", aggregation=True)
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dalli)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_halva(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Halva к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        halva = self.app.dicts.form_connection_type(delivery_service_code="Halva")
        halva["data"]["client"] = os.getenv("HALVA_CLIENT_AND_KEY")
        halva["data"]["key"] = os.getenv("HALVA_CLIENT_AND_KEY")
        if aggregation:
            halva = self.app.dicts.form_connection_type(delivery_service_code="Halva", aggregation=True)
        result = self.app.http_method.post(link=self.link_delivery_services(), json=halva)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_kaz_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки KazPost к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        kaz_post = self.app.dicts.form_connection_type(delivery_service_code="KazPost")
        kaz_post["data"]["key"] = os.getenv("KAZ_POST_KEY")
        kaz_post["data"]["intakePostOfficeCode"] = os.getenv("KAZ_POST_INTAKE_POST_OFFICE_CODE")
        kaz_post["data"]["bin"] = os.getenv("KAZ_POST_BIN")
        kaz_post["data"]["counterparty"] = os.getenv("KAZ_POST_COUNTERPARTY")
        kaz_post["data"]["acceptanceEmail"] = os.getenv("KAZ_POST_ACCEPTANCE_EMAIL")
        kaz_post["data"]["agreementDate"] = "2024-01-01"
        kaz_post["data"]["agreementNumber"] = "1234"
        if aggregation:
            kaz_post = self.app.dicts.form_connection_type(delivery_service_code="KazPost", aggregation=True)
        result = self.app.http_method.post(link=self.link_delivery_services(), json=kaz_post)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_alemtat(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки AlemTat к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        alemtat = self.app.dicts.form_connection_type(delivery_service_code="AlemTat")
        alemtat["data"]["apiKey"] = os.getenv("ALEMTAT_KEY")
        alemtat["data"]["card"] = os.getenv("ALEMTAT_CARD")
        alemtat["data"]["contract"] = os.getenv("ALEMTAT_CONTRACT")
        alemtat["data"]["receivingStation"] = os.getenv("ALEMTAT_RECEIVING_STATION")
        if aggregation:
            alemtat = self.app.dicts.form_connection_type(delivery_service_code="AlemTat", aggregation=True)
        result = self.app.http_method.post(link=self.link_delivery_services(), json=alemtat)
        return self.app.http_method.return_result(response=result)

    def post_delivery_services_pony_express(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки PonyExpress к магазину по агрегации.
        :param aggregation: Тип подключения СД по агрегации.
        """
        pony_express = self.app.dicts.form_connection_type(delivery_service_code="PonyExpress")
        pony_express["data"]["accessKey"] = os.getenv("PONY_ACCESS_KEY")
        if aggregation:
            pony_express = self.app.dicts.form_connection_type(delivery_service_code="PonyExpress", aggregation=True)
        result = self.app.http_method.post(link=self.link_delivery_services(), json=pony_express)
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
        patch = self.app.dicts.form_patch_body(op="replace", path="settings.tariffs",
                                               value=self.app.dicts.settings_tariffs(tariffs=tariffs))
        result = self.app.http_method.patch(link=f"{self.link_delivery_services()}/{code}", json=patch)
        return self.app.http_method.return_result(response=result)

    def patch_delivery_services(self, code: str, value: bool = True):
        r"""Метод редактирования полей настройки подключения к СД.
        :param code: Код СД.
        :param value: Скрытие СД из ЛК при False.
        """
        patch = self.app.dicts.form_patch_body(op="replace", path="visibility", value=value)
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
