from random import randrange
import json


class ApiWarehouse:

    def __init__(self, app):
        self.app = app
        self.link = "customer/warehouses"

    @staticmethod
    def json_warehouse(fullname: str = "Виктор Викторович"):
        r"""Json создания склада.
        :param fullname: ФИО contact person по умолчанию 'Виктор Викторович'.
        """
        warehouse = json.dumps(
            {
                "name": f"{randrange(100000, 999999)}",
                "address": {
                    "raw": "115035, г Москва, р-н Замоскворечье, ул Садовническая, д 14 стр 2"
                },
                "lPostWarehouseId": "20537",
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
        r"""Json для редактирования полей склада.
        :param field: Изменяемое поле.
        :param new_value: Новое значения поля.
        """
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

    def post_warehouse(self, fullname: str = "Виктор Викторович"):
        r"""Метод создания нового склада.
        :param fullname: ФИО contact person по умолчанию 'Виктор Викторович'.
        """
        warehouse = self.json_warehouse(fullname=fullname)
        return self.app.http_method.post(link=self.link, data=warehouse)

    def get_warehouses(self):
        """Метод получения списка складов."""
        return self.app.http_method.get(link=self.link)

    def get_warehouse_id(self, warehouse_id: str):
        r"""Метод получения склада по его id.
        :param warehouse_id: Идентификатор склада.
        """
        return self.app.http_method.get(link=f"{self.link}/{warehouse_id}")

    def put_warehouse(self, warehouse_id: str, fullname: str):
        """Метод редактирования склада.
        :param warehouse_id: Идентификатор склада.
        :param fullname: ФИО contact person.
        """
        warehouse = self.json_warehouse(fullname=fullname)
        return self.app.http_method.put(link=f"{self.link}/{warehouse_id}", data=warehouse)

    def patch_warehouse(self, warehouse_id: str):
        r"""Метод делает склад не активным.
        :param warehouse_id: Идентификатор склада.
        """
        body = self.json_field_changes(field="visibility", new_value=False)
        return self.app.http_method.patch(link=f"{self.link}/{warehouse_id}", data=body)

    def delete_warehouse(self, warehouse_id: str):
        r"""Метод удаления склада.
        :param warehouse_id: Идентификатор склада.
        """
        return self.app.http_method.delete(link=f"{self.link}/{warehouse_id}")
    
    def getting_list_warehouse_ids(self):
        """Метод получения списка id складов."""
        warehouses_id_list = []
        warehouses_list = self.get_warehouses()
        for warehouse in warehouses_list.json():
            warehouses_id_list.append(warehouse["id"])
        return warehouses_id_list
