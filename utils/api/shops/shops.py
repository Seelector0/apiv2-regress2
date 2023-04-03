from random import randrange
import json


class ApiShop:

    def __init__(self, app):
        self.app = app
        self.link = "/customer/shops"

    @staticmethod
    def json_shop(shop_name: str = f"INT{randrange(100000, 999999)}",
                  url_shop: str = f"integration-shop{randrange(1000, 9999)}.ru",
                  phone: str = f"7916{randrange(1000000, 9999999)}",
                  contact_person: str = "Иванов Иван Иванович"):
        """Json создания магазина"""
        json_create_shop = json.dumps(
            {
                "name": shop_name,
                "uri": url_shop,
                "phone": phone,
                "sender": contact_person
            }
        )
        return json_create_shop

    def post_shop(self):
        """Метод создание магазина"""
        new_shop = self.json_shop()
        return self.app.http_method.post(link=self.link, data=new_shop)

    def get_shops(self):
        """Метод получения списка магазинов"""
        return self.app.http_method.get(link=self.link)

    def get_shop_id(self, shop_id: str):
        """Метод получения магазина по его id"""
        return self.app.http_method.get(link=f"{self.link}/{shop_id}")

    def put_shop(self, shop_id: str, json_shop):
        """Метод редактирования магазина"""
        shop = self.json_shop(json_shop)
        return self.app.http_method.put(link=f"{self.link}/{shop_id}", data=shop)

    def patch_shop(self, shop_id: str, value: bool):
        """Метод делает магазин видимым или не видимым для ЛК"""
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

    def getting_list_shop_ids(self):
        """Метод получения id магазинов"""
        shops_id_list = []
        shops_list = self.get_shops()
        for shop in shops_list.json():
            shops_id_list.append(shop["id"])
        return shops_id_list
