from fixture.database import DataBase
from environment import ENV_OBJECT
from random import randrange
import json


class ApiShop:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())
        self.link = "customer/shops"

    def post_shop(self, shop_name: str = f"INT{randrange(100000, 999999)}",
                  url_shop: str = f"integration-shop{randrange(1000, 9999)}.ru",
                  phone: str = f"7916{randrange(1000000, 9999999)}",
                  contact_person: str = "Иванов Иван Иванович"):
        r"""Json создания магазина.
        :param shop_name: Название магазина можно написать своё.
        :param url_shop: URL адрес магазина можно написать своё.
        :param phone: Телефон контактного лица магазина можно написать своё.
        :param contact_person: ФИО контактного лица магазина можно написать своё.
        """
        json_create_shop = json.dumps(
            {
                "name": shop_name,
                "uri": url_shop,
                "phone": phone,
                "sender": contact_person
            }
        )
        return self.app.http_method.post(link=self.link, data=json_create_shop)

    def get_shops(self):
        """Метод получения списка магазинов."""
        return self.app.http_method.get(link=self.link)

    def get_shop_id(self, shop_id: str):
        """Метод получения магазина по его id.
        :param shop_id: Идентификатор магазина.
        """
        return self.app.http_method.get(link=f"{self.link}/{shop_id}")

    def put_shop(self, shop_id: str, shop_name: str, shop_url: str, contact_person: str, phone: str):
        """Метод обновления магазина."""
        get_shop = self.get_shop_id(shop_id=shop_id)
        shop = get_shop.json()
        shop["name"] = shop_name
        shop["uri"] = shop_url
        shop["sender"] = contact_person
        shop["phone"] = phone
        body = json.dumps(shop)
        return self.app.http_method.put(link=f"{self.link}/{shop_id}", data=body)

    def patch_shop(self, shop_id: str, value: bool = True):
        r"""Метод делает магазин видимым или не видимым для ЛК.
        :param shop_id: Идентификатор магазина.
        :param value: Флаг скрывает магазин из ЛК при значение False.
        """
        body = json.dumps(
            [
                {
                    "op": "replace",
                    "path": "visibility",
                    "value": value
                }
            ]
        )
        return self.app.http_method.patch(link=f"{self.link}/{shop_id}", data=body)
