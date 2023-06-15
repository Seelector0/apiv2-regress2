from random import randrange
import json


class ApiWarehouse:

    def __init__(self, app):
        self.app = app
        self.link = "customer/warehouses"

    def post_warehouse(self):
        """Json создания склада."""
        warehouse = json.dumps(
            {
                "name": f"{randrange(100000, 999999)}",
                "address": {
                    "raw": "115035, г Москва, р-н Замоскворечье, ул Садовническая, д 14 стр 2"
                },
                "lPostWarehouseId": "20537",
                "pickup": True,
                "contact": {
                    "fullName": "Виктор Викторович",
                    "phone": f"+7910{randrange(1000000, 9999999)}",
                    "email": "test@email.ru"
                }
            }
        )
        return self.app.http_method.post(link=self.link, data=warehouse)

    def get_warehouses(self):
        """Метод получения списка складов."""
        return self.app.http_method.get(link=self.link)

    def get_warehouse_id(self, warehouse_id: str):
        r"""Метод получения склада по его id.
        :param warehouse_id: Идентификатор склада.
        """
        return self.app.http_method.get(link=f"{self.link}/{warehouse_id}")

    def put_warehouse(self, warehouse_id: str, name: str, pickup: bool, comment: str, l_post_warehouse_id: str,
                      dpd_pickup_num: str, address: str, full_name: str, phone: str, email: str, working_time: dict):
        r"""Метод обновления склада.
        :param warehouse_id: Идентификатор склада.
        :param name: Название склада.
        :param pickup: Флаг, что службы доставки забирают заказы с этого склад.
        :param comment: Комментарий для курьера.
        :param l_post_warehouse_id: Id склада СД LPost нужен для создания заказов по СД LPost.
        :param dpd_pickup_num: Номер регулярного заказа DPD.
        :param address: Адрес склада.
        :param full_name: ФИО контактного лица склада.
        :param phone: Телефон контактного лица склада.
        :param email: Email контактного лица склада.
        :param working_time: Время работы склада.
        """
        get_warehouse = self.get_warehouse_id(warehouse_id=warehouse_id)
        warehouse = get_warehouse.json()
        warehouse["name"] = name
        warehouse["pickup"] = pickup
        warehouse["comment"] = comment
        warehouse["lPostWarehouseId"] = l_post_warehouse_id
        warehouse["dpdPickupNum"] = dpd_pickup_num
        warehouse["address"]["raw"] = address
        warehouse["contact"]["fullName"] = full_name
        warehouse["contact"]["phone"] = phone
        warehouse["contact"]["email"] = email
        warehouse["workingTime"] = working_time
        json_patch_warehouse = json.dumps(warehouse)
        return self.app.http_method.put(link=f"{self.link}/{warehouse_id}", data=json_patch_warehouse)

    def patch_warehouse(self, warehouse_id: str, path: str, value):
        r"""Метод для редактирования полей склада.
        :param warehouse_id: Идентификатор склада.
        :param path: Изменяемое поле.
        :param value: Новое значение поля.
        """
        if path == "visibility":
            value: bool = value
            body = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "visibility",
                        "value": value
                    }
                ]
            )
        elif path == "comment":
            value: str = value
            body = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "comment",
                        "value": value
                    }
                ]
            )
        elif path == "pickup":
            value: bool = value
            body = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "pickup",
                        "value": value
                    }
                ]
            )
        elif path == "dpdPickupNum":
            value: str = value
            body = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "dpdPickupNum",
                        "value": value
                    }
                ]
            )
        elif path == "fullName":
            value: str = value
            body = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "contact.fullName",
                        "value": value
                    }
                ]
            )
        elif path == "phone":
            value: str = value
            body = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "contact.phone",
                        "value": value
                    }
                ]
            )
        elif path == "email":
            value: str = value
            body = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "contact.email",
                        "value": value
                    }
                ]
            )
        elif path == "workingTime":
            value: dict = value
            body = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "workingTime",
                        "value": value
                    }
                ]
            )
        elif path == "lPostWarehouseId":
            value: str = value
            body = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "lPostWarehouseId",
                        "value": value
                    }
                ]
            )
        else:
            raise ValueError(f"Выбрана не верная операция {path}")
        return self.app.http_method.patch(link=f"{self.link}/{warehouse_id}", data=body)

    def delete_warehouse(self, warehouse_id: str):
        r"""Метод удаления склада.
        :param warehouse_id: Идентификатор склада.
        """
        return self.app.http_method.delete(link=f"{self.link}/{warehouse_id}")
