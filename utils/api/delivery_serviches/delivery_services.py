from dotenv import load_dotenv, find_dotenv
from fixture.database import DataBase
from environment import ENV_OBJECT
import allure
import json
import os


class ApiDeliveryServices:

    load_dotenv(find_dotenv())

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())

    @staticmethod
    def integration(delivery_service_code):
        r"""Настройки по интеграции.
        :param delivery_service_code: Код службы доставки.
        """
        integration = {
            "deliveryServiceCode": delivery_service_code,
            "data": {
                "type": "integration"
            }
        }
        return integration

    @staticmethod
    def aggregation(delivery_service_code):
        r"""Настройки по агрегации.
        :param delivery_service_code: Код службы доставки.
        """
        aggregation = {
            "deliveryServiceCode": delivery_service_code,
            "data": {
                "type": "aggregation"
            }
        }
        return aggregation

    def link_delivery_services(self):
        """Метод получения ссылки для подключения СД."""
        return f"{self.app.shop.link}/{self.database.metaship.get_list_shops()[0]}/delivery_services"

    def delivery_services_russian_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки RussianPost к магазину
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            russian_post = self.aggregation(delivery_service_code="RussianPost")
            russian_post["data"]["intakePostOfficeCode"] = "101000"
        else:
            russian_post = self.integration(delivery_service_code="RussianPost")
            russian_post["data"]["intakePostOfficeCode"] = "101000"
            russian_post["data"]["token"] = f"{os.getenv('RP_TOKEN')}"
            russian_post["data"]["secret"] = f"{os.getenv('RP_SECRET')}"
        with allure.step(title=f"Requests: {russian_post}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(russian_post))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_topdelivery(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки TopDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            topdelivery = self.aggregation(delivery_service_code="TopDelivery")
        else:
            topdelivery = self.integration(delivery_service_code="TopDelivery")
            topdelivery["data"]["username"] = f"{os.getenv('TD_USER_NAME')}"
            topdelivery["data"]["password"] = f"{os.getenv('TD_PASSWORD')}"
            topdelivery["data"]["basicLogin"] = f"{os.getenv('TD_BASIC_LOGIN')}"
            topdelivery["data"]["basicPassword"] = f"{os.getenv('TD_BASIC_PASSWORD')}"
        with allure.step(title=f"Requests: {topdelivery}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(topdelivery))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_boxberry(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Boxberry к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            boxberry = self.aggregation(delivery_service_code="Boxberry")
            boxberry["data"]["intakeDeliveryPointCode"] = "00127"
        else:
            boxberry = self.integration(delivery_service_code="Boxberry")
            boxberry["data"]["intakeDeliveryPointCode"] = "00127"
            boxberry["data"]["token"] = f"{os.getenv('BB_API_TOKEN')}"
        with allure.step(title=f"Requests: {boxberry}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(boxberry))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_cdek(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Cdek к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            cdek = self.aggregation(delivery_service_code="Cdek")
            cdek["data"]["shipmentPointCode"] = "AKHT1"
        else:
            cdek = self.integration(delivery_service_code="Cdek")
            cdek["data"]["shipmentPointCode"] = "AKHT1"
            cdek["data"]["account"] = f"{os.getenv('CDEK_ACCOUNT')}"
            cdek["data"]["password"] = f"{os.getenv('CDEK_PASSWORD')}"
        with allure.step(title=f"Requests: {cdek}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(cdek))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_drh_logistic(self):
        """Настройки подключения службы доставки DRH Logistic к магазину."""
        drh_logistic = self.integration(delivery_service_code="Drhl")
        drh_logistic["data"]["apiKey"] = f"{os.getenv('DRHL_API_TOKEN')}"
        with allure.step(title=f"Requests: {drh_logistic}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(drh_logistic))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_dpd(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Dpd к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            dpd = self.aggregation(delivery_service_code="Dpd")
            dpd["data"]["intakePointCode"] = "M16"
        else:
            dpd = self.integration(delivery_service_code="Dpd")
            dpd["data"]["clientNumber"] = f"{os.getenv('DPD_CLIENT_NUMBER')}"
            dpd["data"]["clientKey"] = f"{os.getenv('DPD_CLIENT_KEY')}"
            dpd["data"]["intakePointCode"] = "M16"
        with allure.step(title=f"Requests: {dpd}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(dpd))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_cse(self):
        """Настройки подключения службы доставки Cse к магазину."""
        cse = self.integration(delivery_service_code="Cse")
        cse["data"]["login"] = f"{os.getenv('CSE_LOGIN')}"
        cse["data"]["password"] = f"{os.getenv('CSE_PASSWORD')}"
        cse["data"]["token"] = f"{os.getenv('CSE_TOKEN')}"
        with allure.step(title=f"Requests: {cse}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(cse))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_five_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки FivePost к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            five_post = self.aggregation(delivery_service_code="FivePost")
        else:
            five_post = self.integration(delivery_service_code="FivePost")
            five_post["data"]["apiKey"] = f"{os.getenv('FIVE_POST_API_KEY')}"
            five_post["data"]["partnerNumber"] = f"{os.getenv('FIVE_POST_PARTNER_NUMBER')}"
            five_post["data"]["baseWeight"] = 1000
        with allure.step(title=f"Requests: {five_post}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(five_post))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_svyaznoy(self):
        """Настройки подключения службы доставки Svyaznoy к магазину."""
        svyaznoy = self.integration(delivery_service_code="Svyaznoy")
        svyaznoy["data"]["login"] = f"{os.getenv('SL_LOGIN')}"
        svyaznoy["data"]["password"] = f"{os.getenv('SL_PASSWORD')}"
        with allure.step(title=f"Requests: {svyaznoy}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(svyaznoy))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_yandex_go(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки YandexGo к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            yandex_go = self.aggregation(delivery_service_code="YandexGo")
        else:
            yandex_go = self.integration(delivery_service_code="YandexGo")
            yandex_go["data"]["token"] = f"{os.getenv('YANDEX_TOKEN')}"
        with allure.step(title=f"Requests: {yandex_go}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(yandex_go))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_yandex_delivery(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки YandexDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            yandex_delivery = self.aggregation(delivery_service_code="YandexDelivery")
            yandex_delivery["data"]["intakePointCode"] = "807655"
        else:
            yandex_delivery = self.integration(delivery_service_code="YandexDelivery")
            yandex_delivery["data"]["token"] = f"{os.getenv('YANDEX_TOKEN')}"
            yandex_delivery["data"]["intakePointCode"] = "807655"
        with allure.step(title=f"Requests: {yandex_delivery}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(yandex_delivery))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_dostavka_club(self):
        """Настройки подключения службы доставки DostavkaClub к магазину."""
        dostavka_club = self.integration(delivery_service_code="DostavkaClub")
        dostavka_club["data"]["login"] = f"{os.getenv('CLUB_LOGIN')}"
        dostavka_club["data"]["pass"] = f"{os.getenv('CLUB_PASSWORD')}"
        with allure.step(title=f"Requests: {dostavka_club}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(dostavka_club))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_dostavka_guru(self):
        """Настройки подключения службы доставки DostavkaGuru к магазину."""
        dostavka_guru = self.integration(delivery_service_code="DostavkaGuru")
        dostavka_guru["data"]["partnerId"] = int(f"{os.getenv('GURU_PARTNER_ID')}")
        dostavka_guru["data"]["key"] = f"{os.getenv('GURU_KEY')}"
        with allure.step(title=f"Requests: {dostavka_guru}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(dostavka_guru))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_l_post(self):
        """Настройки подключения службы доставки LPost к магазину."""
        l_post = self.integration(delivery_service_code="LPost")
        l_post["data"]["secret"] = f"{os.getenv('L_POST_SECRET')}"
        with allure.step(title=f"Requests: {l_post}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(l_post))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def delivery_services_dalli(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Dalli к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            dalli = self.aggregation(delivery_service_code="Dalli")
        else:
            dalli = self.integration(delivery_service_code="Dalli")
            dalli["data"]["token"] = f"{os.getenv('DALLI_TOKEN')}"
        with allure.step(title=f"Requests: {dalli}"):
            result = self.app.http_method.post(link=self.link_delivery_services(), data=json.dumps(dalli))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def get_delivery_services(self):
        """Метод получения списка выполненных настроек СД к магазину."""
        result = self.app.http_method.get(link=self.link_delivery_services())
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def get_delivery_services_code(self, code: str):
        r"""Получение настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        result = self.app.http_method.get(link=f"{self.link_delivery_services()}/{code}")
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def patch_delivery_services(self, code: str, value: bool = True, tariffs: list = None):
        r"""Метод редактирования полей настройки подключения к СД.
        :param code: Код СД.
        :param value: Скрытие СД из ЛК при False.
        :param tariffs: Список тарифов для редактирования.
        """
        if tariffs:
            patch = [
                {
                    "op": "replace",
                    "path": "settings.tariffs",
                    "value": {
                        "exclude": tariffs,
                        "restrict": None
                    }
                }
            ]
        else:
            patch = [
                {
                    "op": "replace",
                    "path": "visibility",
                    "value": value
                }
            ]
        with allure.step(title=f"Requests: {patch}"):
            result = self.app.http_method.patch(link=f"{self.link_delivery_services()}/{code}", data=json.dumps(patch))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def activate_delivery_service(self, code: str):
        r"""Активация настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        result = self.app.http_method.post(link=f"{self.link_delivery_services()}/{code}/activate")
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def deactivate_delivery_service(self, code: str):
        r"""Деактивация настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        result = self.app.http_method.post(link=f"{self.link_delivery_services()}/{code}/deactivate")
        with allure.step(title=f"Response: {result.json()}"):
            return result
