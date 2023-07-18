from fixture.database import DataBase
from environment import ENV_OBJECT
from random import randrange, randint
import datetime
import allure
import json


class Intakes:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())
        self.link = "intakes"

    def post_intakes(self, delivery_service):
        r"""Метод создание забора.
        :param delivery_service: СД только Boxberry, Cdek, Cse.
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        intakes = {
            "deliveryService": delivery_service,
            "date": str(tomorrow),
            "shop": {
                "id": self.database.metaship.get_list_shops()[0],
                "number": f"intake{randrange(1000000, 9999999)}"
            },
            "comment": "Позвонить за 3 часа до забора!",
            "from": {
                "warehouseId": self.database.metaship.get_list_warehouses()[0]
            },
            "to": {
                "warehouseId": self.database.metaship.get_list_warehouses()[0]
            },
            "dimension": {
                "length": randint(10, 50),
                "width": randint(10, 50),
                "height": randint(10, 50)
            },
            "weight": randint(1, 5),
            "countCargoPlace": 1,
            "time": {
                "from": "12:00",
                "to": "15:00"
            },
            "description": "Классный груз"
        }
        with allure.step(title=f"Requests: {intakes}"):
            result = self.app.http_method.post(link=self.link, data=json.dumps(intakes))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def get_intakes(self):
        """Получение списка заборов."""
        result = self.app.http_method.get(link=self.link)
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def get_intakes_id(self, intakes_id: str):
        r"""Получения информации о заборе по его id.
        :param intakes_id: Идентификатор забора.
        """
        result = self.app.http_method.get(link=f"{self.link}/{intakes_id}")
        if result.status_code == 200:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        else:
            pass
        return result
