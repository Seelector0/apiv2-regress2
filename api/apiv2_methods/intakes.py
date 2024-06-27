

class ApiIntakes:

    def __init__(self, app):
        self.app = app
        self.link = "intakes"

    def post_intakes(self, delivery_service, shop_id, warehouse_id):
        r"""Метод создание забора.
        :param shop_id: Id магазина.
        :param warehouse_id: Id склада.
        :param delivery_service: СД только Boxberry, Cdek, Cse.
        """
        intake = self.app.dicts.form_intakes(delivery_service=delivery_service, shop_id=shop_id,
                                             warehouse_id=warehouse_id)
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
