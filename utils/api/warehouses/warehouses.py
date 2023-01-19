from model.warehouses import Warehouse
from utils.http_methods import HttpMethods
from random import randrange
import json


class ApiWarehouse:

    @staticmethod
    def json_warehouse(fullname: str):
        """Json создания склада"""
        warehouse = json.dumps(
            {
                "name": f"{randrange(100000, 999999)}",
                "address": {
                    "raw": "115035, г Москва, р-н Замоскворечье, ул Садовническая, д 14 стр 2"
                },
                "pickup": False,
                "contact": {
                    "fullName": fullname,
                    "phone": f"+7910{randrange(1000000, 9999999)}",
                    "email": "test@email.ru"
                }
            }
        )
        return warehouse

    @staticmethod
    def json_field_changes(field: str, new_value):
        """Json для редактирования полей склада"""
        body = json.dumps(
            [
                {
                    "op": "replace",
                    "path": field,
                    "value": new_value
                }
            ]
        )
        return body

    @staticmethod
    def create_warehouse(headers: dict, fullname: str):
        """Метод создания нового магазина"""
        warehouse = ApiWarehouse.json_warehouse(fullname=fullname)
        result_post_warehouse = HttpMethods.post(link="/customer/warehouses", data=warehouse, headers=headers)
        return result_post_warehouse

    @staticmethod
    def get_warehouses(headers: dict):
        """Метод получения списка складов"""
        result_get_warehouse = HttpMethods.get(link="/customer/warehouses", headers=headers)
        return result_get_warehouse

    @staticmethod
    def get_warehouse_by_id(headers: dict, warehouse_id: str):
        """Метод получения склада по его id"""
        result_get_warehouse_by_id = HttpMethods.get(link=f"/customer/warehouses/{warehouse_id}", headers=headers)
        return result_get_warehouse_by_id

    @staticmethod
    def put_warehouse(headers: dict, warehouse_id: str, fullname: str):
        """Метод редактирования склада"""
        warehouse = ApiWarehouse.json_warehouse(fullname=fullname)
        result_put_warehouse = HttpMethods.put(link=f"/customer/warehouses/{warehouse_id}", data=warehouse, headers=headers)
        return result_put_warehouse

    @staticmethod
    def patch_warehouse_by_id(headers: dict, warehouse_id: str):
        """Метод делает склад не активным"""
        body = ApiWarehouse.json_field_changes(field="visibility", new_value=False)
        result_patch = HttpMethods.patch(link=f"/customer/warehouses/{warehouse_id}", data=body, headers=headers)
        return result_patch

    @staticmethod
    def delete_warehouse(headers: dict, warehouse_id: str):
        """Метод удаления склада"""
        result_delete = HttpMethods.delete(link=f"/customer/warehouses/{warehouse_id}", headers=headers)
        return result_delete

    @staticmethod
    def get_warehouses_list(headers: dict):
        """Функция собирает список магазинов"""
        warehouses_list = []
        shops = HttpMethods.get(link="/customer/warehouses", headers=headers)
        for element in shops.json():
            warehouse_id = element["id"]
            name = element["name"]
            warehouses_list.append(Warehouse(warehouse_id=warehouse_id, name_warehouse=name))
        return warehouses_list
