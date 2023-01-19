from utils.http_methods import HttpMethods
from model.shops import Shop
from random import randrange
import json


class ApiShop:

    @staticmethod
    def json_shop(shop_name: str):
        shop = json.dumps(
            {
                "name": shop_name,
                "uri": f"integration-shop{randrange(1000, 9999)}.ru",
                "phone": f"7916{randrange(1000000, 9999999)}",
                "sender": "Иванов Иван Иванович"
            }
        )
        return shop

    @staticmethod
    def create_shop(headers: dict, shop_name: str):
        """Создание магазина"""
        shop = ApiShop.json_shop(shop_name=shop_name)
        result_post_shop = HttpMethods.post(link="/customer/shops", data=shop, headers=headers)
        return result_post_shop

    @staticmethod
    def get_shop(headers: dict):
        """Метод получения списка магазинов"""
        result_get_shop = HttpMethods.get(link="/customer/shops", headers=headers)
        return result_get_shop

    @staticmethod
    def get_shop_by_id(headers: dict, shop_id: str):
        """Метод получения магазина по его id"""
        result_get_shop_by_id = HttpMethods.get(link=f"/customer/shops/{shop_id}", headers=headers)
        return result_get_shop_by_id

    @staticmethod
    def put_shop(headers: dict, shop_id: str, shop_name: str):
        """Метод редактирования магазина"""
        shop = ApiShop.json_shop(shop_name=shop_name)
        result_put = HttpMethods.put(link=f"/customer/shops/{shop_id}", data=shop, headers=headers)
        return result_put

    @staticmethod
    def patch_shop(headers: dict, shop_id: str, value: bool):
        """Метод делает магазин не активным"""
        body = json.dumps([
            {
                "op": "replace",
                "path": "visibility",
                "value": value
            }
        ])
        result_patch = HttpMethods.patch(link=f"/customer/shops/{shop_id}", data=body, headers=headers)
        return result_patch

    @staticmethod
    def get_shops_list(headers: dict):
        """Функция собирает список магазинов"""
        shop_list = []
        shops = HttpMethods.get(link="/customer/shops", headers=headers)
        for element in shops.json():
            shop_id = element["id"]
            name = element["name"]
            shop_list.append(Shop(shop_id=shop_id, shop_name=name))
        return shop_list
