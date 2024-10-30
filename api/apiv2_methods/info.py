import datetime


class ApiInfo:

    def __init__(self, app):
        self.app = app

    def get_delivery_time_schedules(self, shop_id, delivery_service_code: str, tariff_id: str = None, data: str = None,
                                    order_id: str = None):
        r"""Получение интервалов доставки конкретной СД.
        :param shop_id: Id магазина.
        :param delivery_service_code: Код СД.
        :param tariff_id: Атрибут указывающий тип доставки, в котором доступен интервал только для СД Dalli.
        :param data: Желаемая дата доставки.
        :param order_id: Номер заказа, только для СД CDEK.
        """
        if delivery_service_code == "Dalli":
            params = self.app.dicts.form_info_body(shop_id, delivery_service_code=delivery_service_code, data=data)
            params["tariffId"] = tariff_id
        elif delivery_service_code == "TopDelivery":
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            params = self.app.dicts.form_info_body(shop_id, delivery_service_code=delivery_service_code, data=tomorrow)
            params["postalCode"] = "119633"
        elif delivery_service_code == "Cdek":
            params = self.app.dicts.form_delivery_service_code(delivery_service_code=delivery_service_code)
            params["orderId"] = order_id
        else:
            params = self.app.dicts.form_delivery_service_code(delivery_service_code=delivery_service_code)
        result = self.app.http_method.get(link="info/delivery_time_schedules", params=params)
        return self.app.http_method.return_result(response=result)

    def get_delivery_service_points(self, shop_id, delivery_service_code: str, city_raw: str = "г. Москва",
                                    limit: int = 10):
        r"""Получение списка ПВЗ конкретной СД.
        :param shop_id: Id магазина.
        :param delivery_service_code: Код СД.
        :param city_raw: Адресная строка по умолчанию г. Москва.
        :param limit: Максимальное количество возвращаемых пунктов выдачи, по умолчанию 10.
        """
        params = self.app.dicts.form_info_body(shop_id=shop_id, delivery_service_code=delivery_service_code)
        params["cityRaw"] = city_raw
        params["limit"] = limit
        result = self.app.http_method.get(link="customer/info/delivery_service_points", params=params)
        return self.app.http_method.return_result(response=result)

    def get_info_vats(self, delivery_service_code: str):
        r"""Получение списка ставок НДС, которые умеет принимать и обрабатывать конкретная СД.
        :param delivery_service_code: Код СД.
        """
        params = self.app.dicts.form_delivery_service_code(delivery_service_code=delivery_service_code)
        result = self.app.http_method.get(link="info/vats", params=params)
        return self.app.http_method.return_result(response=result)

    def get_intake_offices(self, delivery_service_code: str):
        r"""Получение списка точек сдачи.
        :param delivery_service_code: Код СД.
        """
        params = self.app.dicts.form_delivery_service_code(delivery_service_code=delivery_service_code)
        result = self.app.http_method.get(link="info/intake_offices", params=params)
        return self.app.http_method.return_result(response=result)

    def get_tariffs(self, code):
        r"""Получение информации о тарифах поддерживаемых СД.
        :param code: Код СД.
        """
        result = self.app.http_method.get(link=f"info/{code}/tariffs")
        return self.app.http_method.return_result(response=result)

    def get_info_delivery_service_services(self, code: str):
        """Получение информации о дополнительных услугах поддерживаемых СД.
        :param code: Код СД.
        """
        result = self.app.http_method.get(link=f"info/delivery_service/{code}/services")
        return self.app.http_method.return_result(response=result)

    def get_user_clients(self):
        """Получение списка ключей."""
        result = self.app.http_method.get(link="user/clients")
        return self.app.http_method.return_result(response=result)

    def get_user_clients_id(self, user_id: str):
        r"""Получение информации о ключе подключения по id.
        :param user_id: Идентификатор клиента.
        """
        result = self.app.http_method.get(link=f"user/clients/{user_id}")
        return self.app.http_method.return_result(response=result)

    def get_info_address(self, raw: str = "101000, г Москва"):
        r"""Разбор адреса.
        :param raw: Адрес.
        """
        params = dict(raw=raw)
        result = self.app.http_method.get(link="info/address", params=params)
        return self.app.http_method.return_result(response=result)
