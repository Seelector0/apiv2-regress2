from fixture.database import DataBase
from environment import ENV_OBJECT
from random import randrange
import allure
import json


class ApiShop:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())
        self.link = "customer/shops"

    def post_shop(self):
        """Метод создания магазина."""
        shop = {
            "name": f"INT{randrange(100000, 999999)}",
            "uri": f"integration-shop{randrange(1000, 9999)}.ru",
            "phone": f"7916{randrange(1000000, 9999999)}",
            "sender": "Иванов Иван Иванович"
        }
        with allure.step(f"Requests: {shop}"):
            result = self.app.http_method.post(link=self.link, data=json.dumps(shop))
        with allure.step(f"Response: {result.json()}"):
            return result

    def get_shops(self):
        """Метод получения списка магазинов."""
        result = self.app.http_method.get(link=self.link)
        with allure.step(f"Response: {result.json()}"):
            return result

    def get_shop_id(self, shop_id: str):
        """Метод получения магазина по его id.
        :param shop_id: Идентификатор магазина.
        """
        result = self.app.http_method.get(link=f"{self.link}/{shop_id}")
        with allure.step(f"Response: {result.json()}"):
            return result

    def put_shop(self, shop_id: str, shop_name: str, shop_url: str, contact_person: str, phone: str):
        r"""Метод обновления магазина.
        :param shop_id: Идентификатор магазина.
        :param shop_name: Название магазина
        :param shop_url: URL адрес магазина
        :param contact_person: ФИО контактного лица магазина.
        :param phone: Телефон контактного лица магазина.
        """
        get_shop = self.get_shop_id(shop_id=shop_id)
        shop = get_shop.json()
        shop["name"] = shop_name
        shop["uri"] = shop_url
        shop["sender"] = contact_person
        shop["phone"] = phone
        with allure.step(f"Requests: {shop}"):
            return self.app.http_method.put(link=f"{self.link}/{shop_id}", data=json.dumps(shop))

    def patch_shop(self, shop_id: str, value: bool = True):
        r"""Метод обновления полей магазина.
        :param shop_id: Идентификатор магазина.
        :param value: Флаг скрывает магазин из ЛК.
        """
        patch_shop = [
            {
                "op": "replace",
                "path": "visibility",
                "value": value
            }
        ]
        with allure.step(f"Requests: {patch_shop}"):
            result = self.app.http_method.patch(link=f"{self.link}/{shop_id}", data=json.dumps(patch_shop))
        with allure.step(f"Response: {result.json()}"):
            return result
