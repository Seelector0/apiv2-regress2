from utils.http_methods import HttpMethods
from random import randrange, randint
import json


class ApiOrder:

    @staticmethod
    def json_order(warehouse_id: str, shop_id: str, payment_type: str, type_ds: str, service: str, tariff: str,
                   price: float, declared_value: float, delivery_point_code=None):
        """Json создания заказа"""
        weight = f"{randint(3, 10)}"
        json_create_order = json.dumps({
            "warehouse": {
            "id": f"{warehouse_id}",
            },
            "shop": {
            "id": f"{shop_id}",
            "number": f"{randrange(100000, 999999)}"
            },
            "payment": {
                "type": payment_type,
                "declaredValue": declared_value,
                "deliverySum": 100.24,
            },
            "dimension": {
                "length": f"{randint(15, 50)}",
                "width": f"{randint(15, 50)}",
                "height": f"{randint(15, 50)}"
            },
            "weight": weight,
            "delivery": {
                "type": type_ds,
                "service": service,
                "tariff": tariff,
                "date": "",
                "time": {
                    "from": "",
                    "to": ""
                },
                "deliveryPointCode": delivery_point_code
            },
            "recipient": {
                "fullName": "Филипенко Юрий Павлович",
                "phoneNumber": f"909{randrange(1000000, 9999999)}",
                "address": {
                    "raw": "115035, г Москва, р-н Замоскворечье, Садовническая наб, д 14 стр 2"
                }
            },
            "comment": "",
            "places": [
                {
            "items": [
                {
                    "article": f"ART{randrange(1000000, 9999999)}",
                    "name": "111",
                    "price": price,
                    "count": 1,
                    "weight": weight,
                    "vat": "NO_VAT"
                }
            ]
                }
            ]
        })
        return json_create_order

    @staticmethod
    def create_order(warehouse_id, shop_id, payment_type, type_ds, service, tariff, price, declared_value, headers,
                     delivery_point_code=None):
        """Метод создания заказа"""
        order = ApiOrder.json_order(warehouse_id=warehouse_id, shop_id=shop_id, payment_type=payment_type,
                                    type_ds=type_ds, service=service, tariff=tariff, price=price,
                                    declared_value=declared_value, delivery_point_code=delivery_point_code)
        create_order = HttpMethods.post(link="/orders", data=order, headers=headers)
        return create_order

    @staticmethod
    def get_orders_list(headers: dict):
        """Метод возвращает список заказов"""
        get_order_list = HttpMethods.get(link="/orders", headers=headers)
        return get_order_list

    @staticmethod
    def get_order_by_id(headers: dict, order_id: str):
        """Метод получения информации о заказе по его id"""
        get_odre_by_id = HttpMethods.get(link=f"/orders/{order_id}", headers=headers)
        return get_odre_by_id

    @staticmethod
    def update_order(order_id: str, headers: dict):
        """Метод обновления заказ"""
        pass

    @staticmethod
    def update_fields_order(order_id: str, headers: dict):
        """Метод обновления поля в заказе"""
        pass

    @staticmethod
    def delete_order(order_id: str, headers: dict):
        delete_order = HttpMethods.delete(link=f"/orders/{order_id}", headers=headers)
        return delete_order

    @staticmethod
    def get_order_patches(order_id: str, headers: dict):
        get_order_patches = HttpMethods.get(link=f"/orders/{order_id}/patches", headers=headers)
        return get_order_patches

    @staticmethod
    def get_order_statuses(order_id: str, headers: dict):
        get_order_statuses = HttpMethods.get(link=f"/orders/{order_id}/statuses", headers=headers)
        return get_order_statuses

    @staticmethod
    def get_order_details(order_id: str, headers: dict):
        get_order_details = HttpMethods.get(link=f"/orders/{order_id}/details", headers=headers)
        return get_order_details