

class ApiOffers:

    def __init__(self, app):
        self.app = app

    def get_offers(self, types: str = None, delivery_service_code: str = None, payment_type: str = None,
                   delivery_point_number: str = None, format_: str = None, country_code: str = None):
        r"""Метод для получения списка офферов.
        :param types: Тип запроса офферов 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param delivery_service_code: Код СД.
        :param country_code: Код страны.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param delivery_point_number: Идентификатор точки доставки.
        :param format_: Получение в формате виджета.
        """
        if format_:
            params = self.app.dicts.form_offers(types="DeliveryPoint")
            params["format"] = format_
        else:
            params = self.app.dicts.form_offers(types=types, country_code=country_code)
            params["paymentType"] = payment_type,
            params["deliveryServiceCode"] = delivery_service_code,
            params["deliveryPointNumber"] = delivery_point_number
        result = self.app.http_method.get(link="offers", params=params)
        return self.app.http_method.return_result(response=result)
