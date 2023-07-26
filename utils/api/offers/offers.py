from fixture.database import DataBase
from environment import ENV_OBJECT
from random import randrange
import simplejson.errors
import allure


class ApiOffers:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())

    def get_offers(self, types: str = None, delivery_service_code: str = None, payment_type: str = None,
                   delivery_point_number: str = None, format_: str = None):
        r"""Метод для получения списка офферов.
        :param types: Тип запроса офферов 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param delivery_service_code: Код СД.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param delivery_point_number: Идентификатор точки доставки.
        :param format_: Получение в формате виджета.
        """
        body_offers = {
            "warehouseId": self.database.metaship.get_list_warehouses()[0],
            "shopId": self.database.metaship.get_list_shops()[0],
            "address": "г Москва, пр-кт Мира, д 45 стр 2",
            "declaredValue": randrange(1000, 5000),
            "height": randrange(10, 45),
            "length": randrange(10, 45),
            "width": randrange(10, 45),
            "weight": randrange(1, 10)
        }
        if format_:
            body_offers["types[0]"] = "DeliveryPoint",
            body_offers["format"] = format_
        else:
            body_offers["paymentType"] = payment_type,
            body_offers["types[0]"] = types,
            body_offers["deliveryServiceCode"] = delivery_service_code,
            body_offers["deliveryPointNumber"] = delivery_point_number
        result = self.app.http_method.get(link="offers", params=body_offers)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError:
            raise AssertionError(f"Код ответа: {result.status_code}, Response: {result.requests.body}")
