from random import randrange, randint
import json
import time


class ApiOrder:

    def __init__(self, app):
        self.app = app
        self.link = "/orders"

    def create_order(self, payment_type: str, declared_value, type_ds: str, service: str, price: float,
                     barcode: str = None, data: str = None, length: float = randint(10, 30),
                     width: float = randint(10, 50), height: float = randint(10, 50), weight: float = randint(1, 5),
                     delivery_point_code: str = None, pickup_time_period: str = None, date_pickup: str = None,
                     routes: list = None, tariff: str = None, delivery_time: dict = None,
                     items_declared_value: int = None):
        """Создание заказа"""
        shop_id = self.app.shop.get_shops_id()
        warehouse_id = self.app.warehouse.get_warehouses_id()
        json_order = json.dumps(
            {
                "warehouse": {
                    "id": warehouse_id[0],
                },
                "shop": {
                    "id": shop_id[0],
                    "number": f"{randrange(1000000, 9999999)}",
                    "barcode": barcode,
                },
                "payment": {
                    "type": payment_type,
                    "declaredValue": declared_value,
                    "deliverySum": 100.24,
                },
                "dimension": {
                    "length": length,
                    "width": width,
                    "height": height
                },
                "weight": 0 + weight,
                "delivery": {
                    "type": type_ds,
                    "service": service,
                    "tariff": tariff,
                    "date": data,
                    "time": delivery_time,
                    "deliveryPointCode": delivery_point_code
                },
                "recipient": {
                    "familyName": "Филипенко",
                    "firstName": "Юрий",
                    "secondName": "Павлович",
                    "phoneNumber": f"+7909{randrange(1000000, 9999999)}",
                    "address": {
                        "raw": "129110, г Москва, Мещанский р-н, пр-кт Мира, д 33 к 1"
                    }
                },
                "comment": "",
                "pickupTimePeriod": pickup_time_period,
                "datePickup": date_pickup,
                "routes": routes,
                "places": [
                    {
                        "items": [
                            {
                                "article": f"ART{randrange(1000000, 9999999)}",
                                "name": "Стол",
                                "price": price,
                                "count": 1,
                                "weight": weight,
                                "vat": "0",
                                "declaredValue": items_declared_value,
                            }
                        ]
                    }
                ]
            }
        )
        result_create_order = self.app.http_method.post(link=self.link, data=json_order)
        return result_create_order

    def create_multi_order(self, payment_type: str, declared_value: float, type_ds: str, service: str, data=None,
                           tariff: str = None, delivery_point_code: str = None, pickup_time_period: str = None,
                           delivery_time: dict = None, date_pickup: str = None, length: float = randint(10, 30),
                           width: float = randint(10, 50), height: float = randint(10, 50),
                           weight_1: float = randint(1, 5), weight_2: float = randint(1, 5),
                           shop_number_1: str = f"{randrange(100000, 999999)}",
                           shop_number_2: str = f"{randrange(100000, 999999)}", dimension: dict = None):
        """Создание многоместного заказа"""
        shop_id = self.app.shop.get_shops_id()
        warehouse_id = self.app.warehouse.get_warehouses_id()
        json_multi_order = json.dumps(
            {
                "warehouse": {
                    "id": warehouse_id[0]
                },
                "shop": {
                    "id": shop_id[0],
                    "number": f"{randrange(1000000, 9999999)}",
                    "barcode": f"{randrange(100000000, 999999999)}",
                },
                "payment": {
                    "type": payment_type,
                    "declaredValue": declared_value,
                    "deliverySum": 200
                },
                "dimension": {
                    "length": length,
                    "width": width,
                    "height": height
                },
                "weight": weight_1 + weight_2,
                "delivery": {
                    "type": type_ds,
                    "deliveryPointCode": delivery_point_code,
                    "service": service,
                    "tariff": tariff,
                    "date": data,
                    "time": delivery_time
                },
                "recipient": {
                    "familyName": "Иванов",
                    "firstName": "Иван",
                    "secondName": "Иванович",
                    "phoneNumber": f"+7909{randrange(1000000, 9999999)}",
                    "address": {
                        "raw": "603000, Нижегородская обл, г Нижний Новгород, ул Большая Покровская, д 4"
                    }
                },
                "comment": "",
                "pickupTimePeriod": pickup_time_period,
                "datePickup": date_pickup,
                "places": [
                    {
                        "items": [
                            {
                                "article": f"ART1{randrange(1000000, 9999999)}",
                                "name": "Стол",
                                "price": 1000,
                                "count": 1,
                                "weight": weight_1,
                                "vat": "0"
                            }
                        ],
                        "barcode": f"Box_1{randrange(100000, 999999)}",
                        "shopNumber": shop_number_1,
                        "weight": weight_1,
                        "dimension": dimension
                    },
                    {
                        "items": [
                            {
                                "article": f"ART2{randrange(1000000, 9999999)}",
                                "name": "Стул",
                                "price": 1000,
                                "count": 1,
                                "weight": weight_2,
                                "vat": "0"
                            }
                        ],
                        "barcode": f"Box_2{randrange(100000, 999999)}",
                        "shopNumber": shop_number_2,
                        "weight": weight_2,
                        "dimension": dimension
                    }
                ]
            }
        )
        result_create_multi_order = self.app.http_method.post(link=self.link, data=json_multi_order)
        return result_create_multi_order

    def create_order_from_file(self, format_file: str = None):
        """Метод создания заказа из файла XLSX и XLS формата Почта России или формата MetaShip"""
        link = f"/import{self.link}"
        shop_id = self.app.shop.get_shops_id()
        warehouse_id = self.app.warehouse.get_warehouses_id()
        if format_file == "russian_post":
            json_order_from_file = {
                "shopId": shop_id[0],
                "warehouseId": warehouse_id[0],
                "type": "russian_post"
            }
            file = [
                ("file", ("ПочтаПартия_20220614_.xls", open("/home/fox140/тесты/ПочтаПартия_20220614_.xls", "rb"),
                          "application/vnd.ms-excel"))
            ]
        else:
            json_order_from_file = {
                "shopId": shop_id[0],
                "warehouseId": warehouse_id[0]
            }
            file = [
                ("file", ("ПочтаПартия_20220614_.xls", open("/home/fox140/тесты/ПочтаПартия_20220614_.xls", "rb"),
                          "application/vnd.ms-excel"))
            ]
        result_order_from_file = self.app.http_method.post(link=link, data=json_order_from_file, files=file)
        return result_order_from_file

    def search_order(self, query: str):
        """Метод поиска по заказам"""
        search = {
            "query": query
        }
        search_order = self.app.http_method.get(link=f"{self.link}/search", params=search)
        return search_order

    def get_orders(self):
        """Метод возвращает список заказов"""
        result_get_order_list = self.app.http_method.get(link=self.link)
        return result_get_order_list

    def get_order_by_id(self, order_id: str, sec: float = 0):
        """Метод получения информации о заказе по его id"""
        time.sleep(sec)
        result_get_odre_by_id = self.app.http_method.get(link=f"{self.link}/{order_id}")
        return result_get_odre_by_id

    def update_order(self, order_id: str, weight: str, length: str, width: str, height: str, declared_value: str,
                     family_name: str):
        """Метод обновления заказ (PUT)"""
        result_get_order_by_id = self.get_order_by_id(order_id=order_id)
        body_order = result_get_order_by_id.json()["data"]["request"]
        body_order["weight"] = weight
        body_order["dimension"]["length"] = length
        body_order["dimension"]["width"] = width
        body_order["dimension"]["height"] = height
        body_order["payment"]["declaredValue"] = declared_value
        body_order["recipient"]["familyName"] = family_name
        body = json.dumps(body_order)
        result_put_order = self.app.http_method.put(link=f"{self.link}/{order_id}", data=body)
        return result_put_order

    def update_field_order(self, order_id: str, path: str = None, shop_number_3: str = f"{randrange(100000, 999999)}",
                           weight_3: float = randint(1, 5), weight_4: float = randint(1, 5), dimension: dict = None):
        """Метод обновления поля в заказе и добавление места (PATCH)"""
        result_get_order_by_id = self.get_order_by_id(order_id=order_id)
        items_1 = result_get_order_by_id.json()["data"]["request"]["places"]
        if path == "places":
            json_path_order = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "places",
                        "value": [
                            *items_1,
                            {
                                "items": [
                                    {
                                        "article": f"ART_3{randrange(1000000, 9999999)}",
                                        "name": "Пуфик",
                                        "price": 1000,
                                        "count": 1,
                                        "weight": weight_3,
                                        "vat": "NO_VAT"
                                    }
                                ],
                                "barcode": f"Box_3{randrange(100000, 999999)}",
                                "shopNumber": shop_number_3,
                                "weight": weight_3,
                                "dimension": dimension
                            }
                        ]
                    }
                ]
            )
        else:
            json_path_order = json.dumps(
                [
                    {
                        "op": "add",
                        "path": "places",
                        "value": [
                            {
                                "barcode": f"Box_3{randrange(100000, 999999)}",
                                "weight": weight_3,
                                "dimension": {
                                    "length": randint(10, 30),
                                    "width": randint(10, 50),
                                    "height": randint(10, 50)
                                }
                            },
                            {
                                "barcode": f"Box_4{randrange(100000, 999999)}",
                                "weight": weight_4,
                                "dimension": {
                                    "length": randint(10, 30),
                                    "width": randint(10, 50),
                                    "height": randint(10, 50)
                                }
                            }
                        ]
                    }
                ]
            )
        result_patch = self.app.http_method.patch(link=f"{self.link}/{order_id}", data=json_path_order)
        return result_patch

    def delete_order(self, order_id: str):
        """Метод удаления заказа"""
        result_delete_order = self.app.http_method.delete(link=f"{self.link}/{order_id}")
        return result_delete_order

    def get_order_patches(self, order_id: str):
        """Получение PATCH изменений по заказу"""
        result_order_patches = self.app.http_method.get(link=f"{self.link}/{order_id}/patches")
        return result_order_patches

    def get_order_statuses(self, order_id: str):
        """Получение информации об истории изменения статусов заказа"""
        result_order_statuses = self.app.http_method.get(link=f"{self.link}/{order_id}/statuses")
        return result_order_statuses

    def get_order_details(self, order_id: str):
        """Получение подробной информации о заказе"""
        result_order_details = self.app.http_method.get(link=f"{self.link}/{order_id}/details")
        return result_order_details

    def get_orders_id(self):
        """Метод получения id заказов не в партии"""
        orders_id_list = []
        order_list = self.get_orders()
        for order in order_list.json():
            if order["status"] == "created":
                orders_id_list.append(order["id"])
        return orders_id_list
