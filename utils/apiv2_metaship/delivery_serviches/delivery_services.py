from utils.dicts import DICT_OBJECT
from dotenv import load_dotenv, find_dotenv
from fixture.database import DataBase
from environment import ENV_OBJECT
import requests.exceptions
import simplejson.errors
import allure
import os


class ApiDeliveryServices:

    load_dotenv(find_dotenv())

    def __init__(self, app):
        self.app = app
        self.database_connections = DataBase(database=ENV_OBJECT.db_connections())

    def link_delivery_services(self):
        """Метод получения ссылки для подключения СД."""
        return f"{self.app.shop.link}/{self.database_connections.metaship.get_list_shops()[0]}/delivery_services"

    def delivery_services_russian_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки RussianPost к магазину
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            russian_post = DICT_OBJECT.form_connection_type(delivery_service_code="RussianPost", aggregation=True)
        else:
            russian_post = DICT_OBJECT.form_connection_type(delivery_service_code="RussianPost")
            russian_post["data"]["token"] = f"{os.getenv('RP_TOKEN')}"
            russian_post["data"]["secret"] = f"{os.getenv('RP_SECRET')}"
        russian_post["data"]["intakePostOfficeCode"] = "101000"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=russian_post)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_topdelivery(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки TopDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            topdelivery = DICT_OBJECT.form_connection_type(delivery_service_code="TopDelivery", aggregation=True)
        else:
            topdelivery = DICT_OBJECT.form_connection_type(delivery_service_code="TopDelivery")
            topdelivery["data"]["username"] = f"{os.getenv('TD_USER_NAME')}"
            topdelivery["data"]["password"] = f"{os.getenv('TD_PASSWORD')}"
            topdelivery["data"]["basicLogin"] = f"{os.getenv('TD_BASIC_LOGIN')}"
            topdelivery["data"]["basicPassword"] = f"{os.getenv('TD_BASIC_PASSWORD')}"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=topdelivery)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_boxberry(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Boxberry к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            boxberry = DICT_OBJECT.form_connection_type(delivery_service_code="Boxberry", aggregation=True)
        else:
            boxberry = DICT_OBJECT.form_connection_type(delivery_service_code="Boxberry")
            boxberry["data"]["token"] = f"{os.getenv('BB_API_TOKEN')}"
        boxberry["data"]["intakeDeliveryPointCode"] = "00127"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=boxberry)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_cdek(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Cdek к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            cdek = DICT_OBJECT.form_connection_type(delivery_service_code="Cdek", aggregation=True)
        else:
            cdek = DICT_OBJECT.form_connection_type(delivery_service_code="Cdek")
            cdek["data"]["account"] = f"{os.getenv('CDEK_ACCOUNT')}"
            cdek["data"]["password"] = f"{os.getenv('CDEK_PASSWORD')}"
        cdek["data"]["shipmentPointCode"] = "AKHT1"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=cdek)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_dpd(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Dpd к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            dpd = DICT_OBJECT.form_connection_type(delivery_service_code="Dpd", aggregation=True)
        else:
            dpd = DICT_OBJECT.form_connection_type(delivery_service_code="Dpd")
            dpd["data"]["clientNumber"] = f"{os.getenv('DPD_CLIENT_NUMBER')}"
            dpd["data"]["clientKey"] = f"{os.getenv('DPD_CLIENT_KEY')}"
        dpd["data"]["intakePointCode"] = "M16"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dpd)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_cse(self):
        """Настройки подключения службы доставки Cse к магазину."""
        cse = DICT_OBJECT.form_connection_type(delivery_service_code="Cse")
        cse["data"]["login"] = f"{os.getenv('CSE_LOGIN')}"
        cse["data"]["password"] = f"{os.getenv('CSE_PASSWORD')}"
        cse["data"]["token"] = f"{os.getenv('CSE_TOKEN')}"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=cse)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_five_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки FivePost к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            five_post = DICT_OBJECT.form_connection_type(delivery_service_code="FivePost", aggregation=True)
        else:
            five_post = DICT_OBJECT.form_connection_type(delivery_service_code="FivePost")
            five_post["data"]["apiKey"] = f"{os.getenv('FIVE_POST_API_KEY')}"
            five_post["data"]["partnerNumber"] = f"{os.getenv('FIVE_POST_PARTNER_NUMBER')}"
            five_post["data"]["baseWeight"] = 1000
        result = self.app.http_method.post(link=self.link_delivery_services(), json=five_post)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_svyaznoy(self):
        """Настройки подключения службы доставки Svyaznoy к магазину."""
        svyaznoy = DICT_OBJECT.form_connection_type(delivery_service_code="Svyaznoy")
        svyaznoy["data"]["login"] = f"{os.getenv('SL_LOGIN')}"
        svyaznoy["data"]["password"] = f"{os.getenv('SL_PASSWORD')}"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=svyaznoy)
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_yandex_go(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки YandexGo к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            yandex_go = DICT_OBJECT.form_connection_type(delivery_service_code="YandexGo", aggregation=True)
        else:
            yandex_go = DICT_OBJECT.form_connection_type(delivery_service_code="YandexGo")
            yandex_go["data"]["token"] = f"{os.getenv('YANDEX_TOKEN')}"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=yandex_go)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_yandex_delivery(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки YandexDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            yandex_delivery = DICT_OBJECT.form_connection_type(delivery_service_code="YandexDelivery", aggregation=True)
        else:
            yandex_delivery = DICT_OBJECT.form_connection_type(delivery_service_code="YandexDelivery")
            yandex_delivery["data"]["token"] = f"{os.getenv('YANDEX_TOKEN')}"
        yandex_delivery["data"]["intakePointCode"] = "807655"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=yandex_delivery)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_dostavka_club(self):
        """Настройки подключения службы доставки DostavkaClub к магазину."""
        dostavka_club = DICT_OBJECT.form_connection_type(delivery_service_code="DostavkaClub")
        dostavka_club["data"]["login"] = f"{os.getenv('CLUB_LOGIN')}"
        dostavka_club["data"]["pass"] = f"{os.getenv('CLUB_PASSWORD')}"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dostavka_club)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_dostavka_guru(self):
        """Настройки подключения службы доставки DostavkaGuru к магазину."""
        dostavka_guru = DICT_OBJECT.form_connection_type(delivery_service_code="DostavkaGuru")
        dostavka_guru["data"]["partnerId"] = int(f"{os.getenv('GURU_PARTNER_ID')}")
        dostavka_guru["data"]["key"] = f"{os.getenv('GURU_KEY')}"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dostavka_guru)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_l_post(self):
        """Настройки подключения службы доставки LPost к магазину."""
        l_post = DICT_OBJECT.form_connection_type(delivery_service_code="LPost")
        l_post["data"]["secret"] = f"{os.getenv('L_POST_SECRET')}"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=l_post)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_services_dalli(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Dalli к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            dalli = DICT_OBJECT.form_connection_type(delivery_service_code="Dalli", aggregation=True)
        else:
            dalli = DICT_OBJECT.form_connection_type(delivery_service_code="Dalli")
            dalli["data"]["token"] = f"{os.getenv('DALLI_TOKEN')}"
        result = self.app.http_method.post(link=self.link_delivery_services(), json=dalli)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_delivery_services(self):
        """Метод получения списка выполненных настроек СД к магазину."""
        result = self.app.http_method.get(link=self.link_delivery_services())
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_delivery_services_code(self, code: str):
        r"""Получение настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        result = self.app.http_method.get(link=f"{self.link_delivery_services()}/{code}")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def patch_delivery_services_tariffs(self, code: str, tariffs):
        r"""Метод редактирования тарифов СД.
        :param code: Код СД.
        :param tariffs: Тарифы СД.
        """
        patch = DICT_OBJECT.form_patch_body(op="replace", path="settings.tariffs", value={
            "exclude": tariffs,
            "restrict": None
            })
        result = self.app.http_method.patch(link=f"{self.link_delivery_services()}/{code}", json=patch)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def patch_delivery_services(self, code: str, value: bool = True):
        r"""Метод редактирования полей настройки подключения к СД.
        :param code: Код СД.
        :param value: Скрытие СД из ЛК при False.
        """
        patch = DICT_OBJECT.form_patch_body(op="replace", path="visibility", value=value)
        result = self.app.http_method.patch(link=f"{self.link_delivery_services()}/{code}", json=patch)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def activate_delivery_service(self, code: str):
        r"""Активация настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        return self.app.http_method.post(link=f"{self.link_delivery_services()}/{code}/activate")

    def deactivate_delivery_service(self, code: str):
        r"""Деактивация настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        return self.app.http_method.post(link=f"{self.link_delivery_services()}/{code}/deactivate")
