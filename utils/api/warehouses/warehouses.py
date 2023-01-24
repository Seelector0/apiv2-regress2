from random import randrange
import json


class ApiWarehouse:

    def __init__(self, app):
        self.app = app

    def json_warehouse(self, fullname: str):
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

    def json_field_changes(self, field: str, new_value):
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

    def create_warehouse(self, headers: dict, fullname: str):
        """Метод создания нового магазина"""
        warehouse = self.json_warehouse(fullname=fullname)
        result_post_warehouse = self.app.http_method.post(link="/customer/warehouses", data=warehouse, headers=headers)
        return result_post_warehouse

    def get_warehouses(self, headers: dict):
        """Метод получения списка складов"""
        result_get_warehouse = self.app.http_method.get(link="/customer/warehouses", headers=headers)
        return result_get_warehouse

    def get_warehouse_by_id(self, headers: dict, warehouse_id: str):
        """Метод получения склада по его id"""
        result_get_warehouse_by_id = self.app.http_method.get(link=f"/customer/warehouses/{warehouse_id}", headers=headers)
        return result_get_warehouse_by_id


    def put_warehouse(self, headers: dict, warehouse_id: str, fullname: str):
        """Метод редактирования склада"""
        warehouse = self.json_warehouse(fullname=fullname)
        result_put_warehouse = self.app.http_method.put(link=f"/customer/warehouses/{warehouse_id}", data=warehouse, headers=headers)
        return result_put_warehouse

    def patch_warehouse_by_id(self, headers: dict, warehouse_id: str):
        """Метод делает склад не активным"""
        body = self.json_field_changes(field="visibility", new_value=False)
        result_patch = self.app.http_method.patch(link=f"/customer/warehouses/{warehouse_id}", data=body, headers=headers)
        return result_patch

    def delete_warehouse(self, headers: dict, warehouse_id: str):
        """Метод удаления склада"""
        result_delete = self.app.http_method.delete(link=f"/customer/warehouses/{warehouse_id}", headers=headers)
        return result_delete
