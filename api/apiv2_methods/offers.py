

class ApiOffers:

    def __init__(self, app):
        self.app = app

    def get_offers(self, shop_id, warehouse_id, types: str = None, delivery_service_code: str = None,
                   payment_type: str = None, delivery_point_number: str = None, intake_point_number: str = None,
                   format_: str = None, country_code: str = None):
        r"""Метод для получения списка офферов.
        :param shop_id: Id магазина.
        :param warehouse_id: Id склада.
        :param types: Тип запроса офферов 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param delivery_service_code: Код СД.
        :param country_code: Код страны.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param delivery_point_number: Идентификатор точки доставки.
        :param intake_point_number: Идентификатор точки сдачи Яндекс.
        :param format_: Получение в формате виджета.
        """
        params = self.app.dicts.form_offers(types=types, country_code=country_code, shop_id=shop_id,
                                            warehouse_id=warehouse_id)
        params["paymentType"] = payment_type,
        params["deliveryServiceCode"] = delivery_service_code,
        params["deliveryPointNumber"] = delivery_point_number
        params["intakePointNumber"] = intake_point_number
        if format_:
            params = self.app.dicts.form_offers(types="DeliveryPoint", shop_id=shop_id, warehouse_id=warehouse_id)
            params["format"] = format_
        result = self.app.http_method.get(link="offers", params=params)
        return self.app.http_method.return_result(response=result)
