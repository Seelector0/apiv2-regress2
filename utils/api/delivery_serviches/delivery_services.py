from dotenv import load_dotenv, find_dotenv
import json
import os


class ApiDeliveryServices:

    load_dotenv(find_dotenv())

    def __init__(self, app):
        self.app = app

    def link_shops(self):
        shop_id = self.app.shop.getting_list_shop_ids()
        return f"/customer/shops/{shop_id[0]}/delivery_services"

    def delivery_services_russian_post(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки Почты России к магазину"""
        if connection_type == "aggregation":
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
        return self.app.http_method.post(link=self.link_shops(), data=json_russian_post)

    def delivery_services_topdelivery(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки TopDelivery к магазину"""
        if connection_type == "aggregation":
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
        return self.app.http_method.post(link=self.link_shops(), data=json_topdelivery)

    def delivery_services_boxberry(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки Boxberry к магазину"""
        if connection_type == "aggregation":
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
        return self.app.http_method.post(link=self.link_shops(), data=json_boxberry)

    def delivery_services_cdek(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки Cdek к магазину"""
        if connection_type == "aggregation":
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
        return self.app.http_method.post(link=self.link_shops(), data=json_cdek)

    def delivery_services_drh_logistic(self):
        """Настройки подключения службы доставки DRH Logistic к магазину"""
        json_drh_logistic = json.dumps(
            {
                "deliveryServiceCode": "Drhl",
                "data": {
                    "type": "integration",
                    "apiKey": f"{os.getenv('DRHL_API_TOKEN')}"
                }
            }
        )
        return self.app.http_method.post(link=self.link_shops(), data=json_drh_logistic)

    def delivery_services_dpd(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки Dpd к магазину"""
        if connection_type == "aggregation":
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
        return self.app.http_method.post(link=self.link_shops(), data=json_dpd)

    def delivery_services_cse(self):
        """Настройки подключения службы доставки Cse к магазину"""
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
        return self.app.http_method.post(link=self.link_shops(), data=json_cse)

    def delivery_services_five_post(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки FivePost к магазину"""
        if connection_type == "aggregation":
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
        return self.app.http_method.post(link=self.link_shops(), data=json_five_post)

    def delivery_services_pick_point(self):
        """Настройки подключения службы доставки PickPoint к магазину"""
        json_pick_point = json.dumps(
            {
                "deliveryServiceCode": "PickPoint",
                "data": {
                    "intakePointCode": None,
                    "login": f"{os.getenv('PICK_POINT_LOGIN')}",
                    "password": f"{os.getenv('PICK_POINT_PASSWORD')}",
                    "agreementNumber": f"{os.getenv('PICK_POINT_AGREEMENT_NUMBER')}",
                    "clientNumber": None
                }
            }
        )
        return self.app.http_method.post(link=self.link_shops(), data=json_pick_point)

    def delivery_services_svyaznoy(self):
        """Настройки подключения службы доставки Svyaznoy к магазину"""
        json_svyaznoy = json.dumps(
            {
                "deliveryServiceCode": "Svyaznoy",
                "data": {
                    "login": f"{os.getenv('SL_LOGIN')}",
                    "password": f"{os.getenv('SL_PASSWORD')}"
                }
            }
        )
        return self.app.http_method.post(link=self.link_shops(), data=json_svyaznoy)

    def delivery_services_yandex_go(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки YandexGo к магазину"""
        if connection_type == "aggregation":
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
        return self.app.http_method.post(link=self.link_shops(), data=json_yandex_go)

    def delivery_services_yandex_delivery(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки YandexDelivery к магазину"""
        if connection_type == "aggregation":
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
        return self.app.http_method.post(link=self.link_shops(), data=json_yandex_delivery)

    def delivery_services_dostavka_club(self):
        """Настройки подключения службы доставки DostavkaClub к магазину"""
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
        return self.app.http_method.post(link=self.link_shops(), data=json_dostavka_club)

    def delivery_services_dostavka_guru(self):
        """Настройки подключения службы доставки DostavkaGuru к магазину"""
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
        return self.app.http_method.post(link=self.link_shops(), data=json_dostavka_guru)

    def get_delivery_services(self):
        """Метод получения списка выполненных настроек СД к магазину"""
        return self.app.http_method.get(link=self.link_shops())

    def get_delivery_services_code(self, code: str):
        """Получение настроек подключения к СД по id магазина"""
        return self.app.http_method.get(link=f"{self.link_shops()}/{code}")

    def patch_fields_delivery_services(self, code: str, value: bool = True, path: str = None, tariffs: list = None):
        """Метод изменения полей СД"""
        if path == "tariffs":
            json_editing = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "settings.tariffs",
                        "value": {
                            "exclude": [tariffs],
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
        return self.app.http_method.patch(link=f"{self.link_shops()}/{code}", data=json_editing)

    def activate_delivery_service(self, code: str):
        """Активация настроек подключения к СД по id магазина"""
        return self.app.http_method.post(link=f"{self.link_shops()}/{code}/activate")

    def deactivate_delivery_service(self, code: str):
        """Деактивация настроек подключения к СД по id магазина"""
        return self.app.http_method.post(link=f"{self.link_shops()}/{code}/deactivate")
