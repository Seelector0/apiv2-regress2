from dotenv import load_dotenv, find_dotenv
from fixture.database import DataBase
from environment import ENV_OBJECT
import json
import os


class ApiDeliveryServices:

    load_dotenv(find_dotenv())

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())

    def link_delivery_services(self):
        """Метод получения ссылки для подключения СД."""
        return f"{self.app.shop.link}/{self.database.metaship.get_list_shops()[0]}/delivery_services"

    def delivery_services_russian_post(self, aggregation: bool = False):
        r"""Настройки подключения службы доставки RussianPost к магазину
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            json_russian_post = json.dumps(
                {
                    "deliveryServiceCode": "RussianPost",
                    "data": {
                        "intakePostOfficeCode": "101000",
                        "type": "aggregation"
                    }
                }
            )
        else:
            json_russian_post = json.dumps(
                {
                    "deliveryServiceCode": "RussianPost",
                    "data": {
                        "token": f"{os.getenv('RP_TOKEN')}",
                        "secret": f"{os.getenv('RP_SECRET')}",
                        "type": "integration",
                        "intakePostOfficeCode": "101000"
                    }
                }
            )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_russian_post)

    def delivery_services_topdelivery(self, aggregation: bool = False):
        r"""Настройки подключения службы доставки TopDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            json_topdelivery = json.dumps(
                {
                    "deliveryServiceCode": "TopDelivery",
                    "data": {
                        "type": "aggregation"
                    }
                }
            )
        else:
            json_topdelivery = json.dumps(
                {
                    "deliveryServiceCode": "TopDelivery",
                    "data": {
                        "username": f"{os.getenv('TD_USER_NAME')}",
                        "password": f"{os.getenv('TD_PASSWORD')}",
                        "basicLogin": f"{os.getenv('TD_BASIC_LOGIN')}",
                        "basicPassword": f"{os.getenv('TD_BASIC_PASSWORD')}",
                        "type": "integration"
                    }
                }
            )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_topdelivery)

    def delivery_services_boxberry(self, aggregation: bool = False):
        r"""Настройки подключения службы доставки Boxberry к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            json_boxberry = json.dumps(
                {
                    "deliveryServiceCode": "Boxberry",
                    "data": {
                        "type": "aggregation",
                        "intakeDeliveryPointCode": "00127"
                    }
                }
            )
        else:
            json_boxberry = json.dumps(
                {
                    "deliveryServiceCode": "Boxberry",
                    "data": {
                        "type": "integration",
                        "intakeDeliveryPointCode": "00127",
                        "token": f"{os.getenv('BB_API_TOKEN')}"
                    }
                }
            )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_boxberry)

    def delivery_services_cdek(self, aggregation: bool = False):
        r"""Настройки подключения службы доставки Cdek к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            json_cdek = json.dumps(
                {
                    "deliveryServiceCode": "Cdek",
                    "data": {
                        "type": "aggregation",
                        "shipmentPointCode": "AKHT1"
                    }
                }
            )
        else:
            json_cdek = json.dumps(
                {
                    "deliveryServiceCode": "Cdek",
                    "data": {
                        "type": "integration",
                        "account": f"{os.getenv('CDEK_ACCOUNT')}",
                        "password": f"{os.getenv('CDEK_PASSWORD')}",
                        "shipmentPointCode": "AKHT1"
                    }
                }
            )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_cdek)

    def delivery_services_drh_logistic(self):
        """Настройки подключения службы доставки DRH Logistic к магазину."""
        json_drh_logistic = json.dumps(
            {
                "deliveryServiceCode": "Drhl",
                "data": {
                    "type": "integration",
                    "apiKey": f"{os.getenv('DRHL_API_TOKEN')}"
                }
            }
        )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_drh_logistic)

    def delivery_services_dpd(self, aggregation: bool = False):
        r"""Настройки подключения службы доставки Dpd к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            json_dpd = json.dumps(
                {
                    "deliveryServiceCode": "Dpd",
                    "data": {
                        "type": "aggregation",
                        "intakePointCode": "M16"
                    }
                }
            )
        else:
            json_dpd = json.dumps(
                {
                    "deliveryServiceCode": "Dpd",
                    "data": {
                        "type": "integration",
                        "clientNumber": f"{os.getenv('DPD_CLIENT_NUMBER')}",
                        "clientKey": f"{os.getenv('DPD_CLIENT_KEY')}",
                        "intakePointCode": "M16"
                    }
                }
            )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_dpd)

    def delivery_services_cse(self):
        """Настройки подключения службы доставки Cse к магазину."""
        json_cse = json.dumps(
            {
                "deliveryServiceCode": "Cse",
                "data": {
                    "login": f"{os.getenv('CSE_LOGIN')}",
                    "password": f"{os.getenv('CSE_PASSWORD')}",
                    "token": f"{os.getenv('CSE_TOKEN')}"
                }
            }
        )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_cse)

    def delivery_services_five_post(self, aggregation: bool = False):
        r"""Настройки подключения службы доставки FivePost к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            json_five_post = json.dumps(
                {
                    "deliveryServiceCode": "FivePost",
                    "data": {
                        "type": "aggregation"
                    }
                }
            )
        else:
            json_five_post = json.dumps(
                {
                    "deliveryServiceCode": "FivePost",
                    "data": {
                        "apiKey": f"{os.getenv('FIVE_POST_API_KEY')}",
                        "partnerNumber": f"{os.getenv('FIVE_POST_PARTNER_NUMBER')}",
                        "baseWeight": 1000,
                        "type": "integration"
                    }
                }
            )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_five_post)

    def delivery_services_svyaznoy(self):
        """Настройки подключения службы доставки Svyaznoy к магазину."""
        json_svyaznoy = json.dumps(
            {
                "deliveryServiceCode": "Svyaznoy",
                "data": {
                    "login": f"{os.getenv('SL_LOGIN')}",
                    "password": f"{os.getenv('SL_PASSWORD')}"
                }
            }
        )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_svyaznoy)

    def delivery_services_yandex_go(self, aggregation: bool = False):
        r"""Настройки подключения службы доставки YandexGo к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            json_yandex_go = json.dumps(
                {
                    "deliveryServiceCode": "YandexGo",
                    "data": {
                        "type": "aggregation"
                    }
                }
            )
        else:
            json_yandex_go = json.dumps(
                {
                    "deliveryServiceCode": "YandexGo",
                    "data": {
                        "token": f"{os.getenv('YANDEX_TOKEN')}",
                        "type": "integration"
                    }
                }
            )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_yandex_go)

    def delivery_services_yandex_delivery(self, aggregation: bool = False):
        r"""Настройки подключения службы доставки YandexDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            json_yandex_delivery = json.dumps(
                {
                    "deliveryServiceCode": "YandexDelivery",
                    "data": {
                        "type": "aggregation",
                        "intakePointCode": "807655"
                    }
                }
            )
        else:
            json_yandex_delivery = json.dumps(
                {
                    "deliveryServiceCode": "YandexDelivery",
                    "data": {
                        "token": f"{os.getenv('YANDEX_TOKEN')}",
                        "type": "integration",
                        "intakePointCode": "807655"
                    }
                }
            )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_yandex_delivery)

    def delivery_services_dostavka_club(self):
        """Настройки подключения службы доставки DostavkaClub к магазину."""
        json_dostavka_club = json.dumps(
            {
                "deliveryServiceCode": "DostavkaClub",
                "data": {
                    "type": "integration",
                    "login": f"{os.getenv('CLUB_LOGIN')}",
                    "pass": f"{os.getenv('CLUB_PASSWORD')}"
                }
            }
        )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_dostavka_club)

    def delivery_services_dostavka_guru(self):
        """Настройки подключения службы доставки DostavkaGuru к магазину."""
        json_dostavka_guru = json.dumps(
            {
                "deliveryServiceCode": "DostavkaGuru",
                "data": {
                    "type": "integration",
                    "partnerId": int(f"{os.getenv('GURU_PARTNER_ID')}"),
                    "key": f"{os.getenv('GURU_KEY')}"
                }
            }
        )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_dostavka_guru)

    def delivery_services_l_post(self):
        """Настройки подключения службы доставки LPost к магазину."""
        json_l_post = json.dumps(
            {
                "deliveryServiceCode": "LPost",
                "data": {
                    "secret": f"{os.getenv('L_POST_SECRET')}"
                }
            }
        )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_l_post)

    def delivery_services_dalli(self, aggregation: bool = False):
        r"""Настройки подключения службы доставки Dalli к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        if aggregation is True:
            json_dalli = json.dumps(
                {
                    "deliveryServiceCode": "Dalli",
                    "data": {
                        "type": "aggregation",
                    }
                }
            )
        else:
            json_dalli = json.dumps(
                {
                    "deliveryServiceCode": "Dalli",
                    "data": {
                        "type": "integration",
                    }
                }
            )
        return self.app.http_method.post(link=self.link_delivery_services(), data=json_dalli)

    def get_delivery_services(self):
        """Метод получения списка выполненных настроек СД к магазину."""
        return self.app.http_method.get(link=self.link_delivery_services())

    def get_delivery_services_code(self, code: str):
        r"""Получение настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        return self.app.http_method.get(link=f"{self.link_delivery_services()}/{code}")

    def patch_delivery_services(self, code: str, value: bool = True, path: str = None, tariffs: list = None):
        r"""Метод редактирования полей настройки подключения к СД.
        :param code: Код СД.
        :param value: Скрытие СД из ЛК при False.
        :param path: Изменяемое поле в СД.
        :param tariffs: Список тарифов для редактирования.
        """
        if path == "tariffs":
            json_editing = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "settings.tariffs",
                        "value": {
                            "exclude": tariffs,
                            "restrict": None
                        }
                    }
                ]
            )
        else:
            json_editing = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "visibility",
                        "value": value
                    }
                ]
            )
        return self.app.http_method.patch(link=f"{self.link_delivery_services()}/{code}", data=json_editing)

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
