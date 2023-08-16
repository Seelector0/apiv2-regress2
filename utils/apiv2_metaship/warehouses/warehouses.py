from utils.json_fixture import Body
from random import randrange
import requests.exceptions
import simplejson.errors
import allure


class ApiWarehouse:

    def __init__(self, app):
        self.app = app
        self.link = "customer/warehouses"

    def post_warehouse(self):
        """Метод создания склада."""
        warehouse = {
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
        result = self.app.http_method.post(link=self.link, data=warehouse)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_warehouses(self):
        """Метод получения списка складов."""
        result = self.app.http_method.get(link=self.link)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_warehouse_id(self, warehouse_id: str):
        r"""Метод получения склада по его id.
        :param warehouse_id: Идентификатор склада.
        """
        result = self.app.http_method.get(link=f"{self.link}/{warehouse_id}")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

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
        return self.app.http_method.put(link=f"{self.link}/{warehouse_id}", data=warehouse)

    def patch_warehouse(self, warehouse_id: str, path: str, value):
        r"""Метод для редактирования полей склада.
        :param warehouse_id: Идентификатор склада.
        :param path: Изменяемое поле.
        :param value: Новое значение поля.
        """
        patch_warehouse = Body.body_patch(op="replace", path=path, value=value)
        result = self.app.http_method.patch(link=f"{self.link}/{warehouse_id}", data=patch_warehouse)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delete_warehouse(self, warehouse_id: str):
        r"""Метод удаления склада.
        :param warehouse_id: Идентификатор склада.
        """
        return self.app.http_method.delete(link=f"{self.link}/{warehouse_id}")
