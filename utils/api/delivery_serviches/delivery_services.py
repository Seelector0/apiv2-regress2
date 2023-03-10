from dotenv import load_dotenv, find_dotenv
import json
import os


class ApiDeliveryServices:

    load_dotenv(find_dotenv())

    def __init__(self, app):
        self.app = app

    @staticmethod
    def link(shop_id):
        return f"/customer/shops/{shop_id}/delivery_services"

    def delivery_services_russian_post(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки Почты России к магазину"""
        shop_id = self.app.shop.get_shops_id()
        if connection_type == "aggregation":
            json_russian_post_aggregation = json.dumps(
                {
                    "deliveryServiceCode": "RussianPost",
                    "data": {
                        "intakePostOfficeCode": "101000",
                        "type": "aggregation"
                    }
                }
            )
            russian_post = self.app.http_method.post(link=self.link(shop_id=shop_id[0]),
                                                     data=json_russian_post_aggregation)
        else:
            json_russian_post_integration = json.dumps(
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
            russian_post = self.app.http_method.post(link=self.link(shop_id=shop_id[0]),
                                                     data=json_russian_post_integration)
        return russian_post

    def delivery_services_topdelivery(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки TopDelivery к магазину"""
        shop_id = self.app.shop.get_shops_id()
        if connection_type == "aggregation":
            json_topdelivery_aggregation = json.dumps(
                {
                    "deliveryServiceCode": "TopDelivery",
                    "data": {
                        "type": "aggregation"
                    }
                }
            )
            topdelivery = self.app.http_method.post(link=self.link(shop_id=shop_id[0]),
                                                    data=json_topdelivery_aggregation)
        else:
            json_topdelivery_integration = json.dumps(
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
            topdelivery = self.app.http_method.post(link=self.link(shop_id=shop_id[0]),
                                                    data=json_topdelivery_integration)
        return topdelivery

    def delivery_services_boxberry(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки Boxberry к магазину"""
        shop_id = self.app.shop.get_shops_id()
        if connection_type == "aggregation":
            json_boxberry_aggregation = json.dumps(
                {
                    "deliveryServiceCode": "Boxberry",
                    "data": {
                        "type": "aggregation",
                        "intakeDeliveryPointCode": "00127"
                    }
                }
            )
            boxberry = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_boxberry_aggregation)
        else:
            json_boxberry_integration = json.dumps(
                {
                    "deliveryServiceCode": "Boxberry",
                    "data": {
                        "type": "integration",
                        "intakeDeliveryPointCode": "00127",
                        "token": f"{os.getenv('BB_API_TOKEN')}"
                    }
                }
            )
            boxberry = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_boxberry_integration)
        return boxberry

    def delivery_services_cdek(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки Cdek к магазину"""
        shop_id = self.app.shop.get_shops_id()
        if connection_type == "aggregation":
            json_cdek_aggregation = json.dumps(
                {
                    "deliveryServiceCode": "Cdek",
                    "data": {
                        "type": "aggregation",
                        "shipmentPointCode": "AKHT1"
                    }
                }
            )
            cdek = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_cdek_aggregation)
        else:
            json_cdek_integration = json.dumps(
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
            cdek = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_cdek_integration)
        return cdek

    def delivery_services_drh_logistic(self):
        """Настройки подключения службы доставки DRH Logistic к магазину"""
        shop_id = self.app.shop.get_shops_id()
        json_drh_logistic = json.dumps(
            {
                "deliveryServiceCode": "Drhl",
                "data": {
                    "type": "integration",
                    "apiKey": f"{os.getenv('DRHL_API_TOKEN')}"
                }
            }
        )
        drh_logistic = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_drh_logistic)
        return drh_logistic

    def delivery_services_dpd(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки Dpd к магазину"""
        shop_id = self.app.shop.get_shops_id()
        if connection_type == "aggregation":
            json_dpd_aggregation = json.dumps(
                {
                    "deliveryServiceCode": "Dpd",
                    "data": {
                        "type": "aggregation",
                        "intakePointCode": "M16"
                    }
                }
            )
            dpd = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_dpd_aggregation)
        else:
            json_dpd_integration = json.dumps(
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
            dpd = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_dpd_integration)
        return dpd

    def delivery_services_cse(self):
        """Настройки подключения службы доставки Cse к магазину"""
        shop_id = self.app.shop.get_shops_id()
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
        cse = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_cse)
        return cse

    def delivery_services_five_post(self, connection_type: str = "integration"):
        """Настройки подключения службы доставки FivePost к магазину"""
        shop_id = self.app.shop.get_shops_id()
        if connection_type == "aggregation":
            json_five_post_aggregation = json.dumps(
                {
                    "deliveryServiceCode": "FivePost",
                    "data": {
                        "type": "aggregation"
                    }
                }
            )
            five_post = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_five_post_aggregation)
        else:
            json_five_post_integration = json.dumps(
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
            five_post = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_five_post_integration)
        return five_post

    def delivery_services_dostavka_club(self):
        """Настройки подключения службы доставки DostavkaClub к магазину"""
        shop_id = self.app.shop.get_shops_id()
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
        dostavka_club = self.app.http_method.post(link=self.link(shop_id=shop_id[0]), data=json_dostavka_club)
        return dostavka_club

    def get_delivery_services(self):
        """Метод получения списка выполненных настроек СД к магазину"""
        shop_id = self.app.shop.get_shops_id()
        get_delivery_services = self.app.http_method.get(link=self.link(shop_id=shop_id[0]))
        return get_delivery_services

    def get_delivery_services_code(self, code: str):
        """Получение настроек подключения к СД по id магазина"""
        shop_id = self.app.shop.get_shops_id()
        result_delivery_services_code = self.app.http_method.get(link=f"{self.link(shop_id=shop_id[0])}/{code}")
        return result_delivery_services_code

    def editing_fields_delivery_services(self, code: str, value: bool):
        """Метод изменения полей СД"""
        shop_id = self.app.shop.get_shops_id()
        json_editing_fields_delivery_services = json.dumps(
            [
                {
                    "op": "replace",
                    "path": "visibility",
                    "value": value
                }
            ]
        )
        result_editing_fields_delivery_services = self.app.http_method.patch(
            link=f"{self.link(shop_id=shop_id[0])}/{code}", data=json_editing_fields_delivery_services)
        return result_editing_fields_delivery_services

    def activate_delivery_service(self, code: str):
        """Активация настроек подключения к СД по id магазина"""
        shop_id = self.app.shop.get_shops_id()
        result_activate_delivery_service = self.app.http_method.post(
            link=f"{self.link(shop_id=shop_id[0])}/{code}/activate")
        return result_activate_delivery_service

    def deactivate_delivery_service(self, code: str):
        """Деактивация настроек подключения к СД по id магазина"""
        shop_id = self.app.shop.get_shops_id()
        result_deactivate_delivery_service = self.app.http_method.post(
            link=f"{self.link(shop_id=shop_id[0])}/{code}/deactivate")
        return result_deactivate_delivery_service
