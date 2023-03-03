from random import randrange
import json


class ApiShop:

    def __init__(self, app):
        self.app = app

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

    def create_shop(self):
        """Создание магазина"""
        new_shop = self.json_shop()
        result_post_shop = self.app.http_method.post(link="/customer/shops", data=new_shop)
        return result_post_shop

    def get_shops(self):
        """Метод получения списка магазинов"""
        result_get_shop = self.app.http_method.get(link="/customer/shops")
        return result_get_shop

    def get_shop_by_id(self, shop_id: str):
        """Метод получения магазина по его id"""
        result_get_shop_by_id = self.app.http_method.get(link=f"/customer/shops/{shop_id}")
        return result_get_shop_by_id

    def put_shop(self, shop_id: str, json_shop):
        """Метод редактирования магазина"""
        shop = self.json_shop(json_shop)
        result_put = self.app.http_method.put(link=f"/customer/shops/{shop_id}", data=shop)
        return result_put

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
        result_patch = self.app.http_method.patch(link=f"/customer/shops/{shop_id}", data=body)
        return result_patch

    def get_shops_id(self):
        """Метод получения id магазинов"""
        shops_id_list = []
        shops_list = self.get_shops()
        for shop in shops_list.json():
            shops_id_list.append(shop["id"])
        return shops_id_list
