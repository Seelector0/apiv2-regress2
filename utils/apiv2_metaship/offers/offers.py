import requests.exceptions
import simplejson.errors
import allure


class ApiOffers:

    def __init__(self, app):
        self.app = app

    def get_offers(self, types: str = None, delivery_service_code: str = None, payment_type: str = None,
                   delivery_point_number: str = None, format_: str = None):
        r"""Метод для получения списка офферов.
        :param types: Тип запроса офферов 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param delivery_service_code: Код СД.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param delivery_point_number: Идентификатор точки доставки.
        :param format_: Получение в формате виджета.
        """
        if format_:
            body_offers = self.app.dict.form_offers(types="DeliveryPoint")
            body_offers["format"] = format_
        else:
            body_offers = self.app.dict.form_offers(types=types)
            body_offers["paymentType"] = payment_type,
            body_offers["deliveryServiceCode"] = delivery_service_code,
            body_offers["deliveryPointNumber"] = delivery_point_number
        result = self.app.http_method.get(link="offers", params=body_offers)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")
