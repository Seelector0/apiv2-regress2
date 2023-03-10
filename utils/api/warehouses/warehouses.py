from random import randrange
import json


class ApiWarehouse:

    def __init__(self, app):
        self.app = app
        self.link = "/customer/warehouses"

    @staticmethod
    def json_warehouse(fullname: str = "Виктор Викторович"):
        """Json создания склада"""
        warehouse = json.dumps(
            {
                "name": f"{randrange(100000, 999999)}",
                "address": {
                    "raw": "115035, г Москва, р-н Замоскворечье, ул Садовническая, д 14 стр 2"
                },
                "pickup": True,
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

    def create_warehouse(self, fullname: str = "Виктор Викторович"):
        """Метод создания нового магазина"""
        warehouse = self.json_warehouse(fullname=fullname)
        result_post_warehouse = self.app.http_method.post(link=self.link, data=warehouse)
        return result_post_warehouse

    def get_warehouses(self):
        """Метод получения списка складов"""
        result_get_warehouse = self.app.http_method.get(link=self.link)
        return result_get_warehouse

    def get_warehouse_by_id(self, warehouse_id: str):
        """Метод получения склада по его id"""
        result_get_warehouse_by_id = self.app.http_method.get(link=f"{self.link}/{warehouse_id}")
        return result_get_warehouse_by_id

    def put_warehouse(self, warehouse_id: str, fullname: str):
        """Метод редактирования склада"""
        warehouse = self.json_warehouse(fullname=fullname)
        result_put_warehouse = self.app.http_method.put(link=f"{self.link}/{warehouse_id}", data=warehouse)
        return result_put_warehouse

    def patch_warehouse_by_id(self, warehouse_id: str):
        """Метод делает склад не активным"""
        body = self.json_field_changes(field="visibility", new_value=False)
        result_patch = self.app.http_method.patch(link=f"{self.link}/{warehouse_id}", data=body)
        return result_patch

    def delete_warehouse(self, warehouse_id: str):
        """Метод удаления склада"""
        result_delete = self.app.http_method.delete(link=f"{self.link}/{warehouse_id}")
        return result_delete
    
    def get_warehouses_id(self):
        """Метод получения id заказов не в партии"""
        warehouses_id_list = []
        warehouses_list = self.get_warehouses()
        for warehouse in warehouses_list.json():
            warehouses_id_list.append(warehouse["id"])
        return warehouses_id_list
