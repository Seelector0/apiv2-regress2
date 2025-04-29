
class ApiIntakes:

    def __init__(self, app):
        self.app = app
        self.link = "intakes"

    def post_intakes(self, delivery_service, shop_id, warehouse_id, date, intake_external_id, parcel_id):
        r"""Метод создание забора.
        :param shop_id: Id магазина.
        :param warehouse_id: Id склада.
        :param date: Дата забора.
        :param delivery_service: СД только Boxberry, Cdek, Cse.
        :param intake_external_id: Внешний идентификатор интервала.
        :param parcel_id: Номер партии.
        """
        intake = self.app.dicts.form_intakes(delivery_service=delivery_service, shop_id=shop_id,
                                             warehouse_id=warehouse_id, date=date,
                                             intake_external_id=intake_external_id, parcel_id=parcel_id)
        result = self.app.http_method.post(link=self.link, json=intake)
        return self.app.http_method.return_result(response=result)

    def get_intakes(self):
        """Получение списка заборов."""
        result = self.app.http_method.get(link=self.link)
        return self.app.http_method.return_result(response=result)

    def get_intakes_id(self, intakes_id: str):
        r"""Получения информации о заборе по его id.
        :param intakes_id: Идентификатор забора.
        """
        result = self.app.http_method.get(link=f"{self.link}/{intakes_id}")
        return self.app.http_method.return_result(response=result)

    def intake_time_schedules(self, shop_id, warehouse_id, delivery_service_code: str):
        r"""Получения информации о заборе по его id.
        :param shop_id: Id магазина.
        :param warehouse_id: Id склада.
        :param delivery_service_code: Идентификатор СД.
        """
        params = self.app.dicts.form_intake_time_schedules(delivery_service_code=delivery_service_code, shop_id=shop_id,
                                                           warehouse_id=warehouse_id)
        result = self.app.http_method.get(link=f"info/intake_time_schedules", params=params)
        return self.app.http_method.return_result(response=result)
