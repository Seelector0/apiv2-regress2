from fixture.database import DataBase
from environment import ENV_OBJECT
from random import randrange, randint
import json


class ApiOrder:

    def __init__(self, app):
        self.app = app
        self.link = "orders"
        self.directory = "folder_with_orders"
        self.method_xls = "application/vnd.ms-excel"
        self.method_xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        self.database = DataBase(database=ENV_OBJECT.db_connections())

    def post_order(self, payment_type: str, declared_value, type_ds: str, service: str, price: float,
                   barcode: str = None, data: str = None, delivery_time: dict = None, length: float = randint(10, 30),
                   width: float = randint(10, 50), height: float = randint(10, 50), weight: float = randint(1, 5),
                   delivery_point_code: str = None, pickup_time_period: str = None, date_pickup: str = None,
                   routes: list = None, tariff: str = None,
                   items_declared_value: int = None):
        r"""Метод создания одноместного заказа.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param declared_value: Объявленная стоимость.
        :param type_ds: Тип доставки 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param service: Код СД.
        :param price: Цена товарной позиции.
        :param barcode: Штрих код заказа.
        :param data: Дата доставки.
        :param delivery_time: Если указанна поле 'data', то delivery_time обязателен для курьерского заказа
        :param length: Длинна.
        :param width: Ширина.
        :param height: Высота.
        :param weight: Вес товарной позиции.
        :param delivery_point_code: Идентификатор точки доставки.
        :param pickup_time_period: Дата привоза на склад.
        :param date_pickup: Временной интервал
        :param routes: Поле обязательное для создания заказа в СД DostavkaGuru.
        :param tariff: Тариф создания заказа.
        :param items_declared_value: Цена товарной позиции.
        """
        json_order = json.dumps(
            {
                "warehouse": {
                    "id": str(self.database.metaship.get_list_warehouses()[0]),
                },
                "shop": {
                    "id": str(self.database.metaship.get_list_shops()[0]),
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
                    "email": "test@mail.ru",
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
        return self.app.http_method.post(link=self.link, data=json_order)

    def post_multi_order(self, payment_type: str, declared_value: float, type_ds: str, service: str, data=None,
                         tariff: str = None, delivery_point_code: str = None, pickup_time_period: str = None,
                         delivery_time: dict = None, date_pickup: str = None, length: float = randint(10, 30),
                         width: float = randint(10, 50), height: float = randint(10, 50),
                         weight_1: float = randint(1, 5), weight_2: float = randint(1, 5),
                         shop_number_1: str = f"{randrange(100000, 999999)}",
                         shop_number_2: str = f"{randrange(100000, 999999)}", dimension: dict = None):
        r"""Метод создания многоместного заказа.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param declared_value: Объявленная стоимость.
        :param type_ds: Тип доставки 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param service: Код СД.
        :param data: Дата доставки.
        :param delivery_time: Если указанна поле 'data', то delivery_time обязателен для курьерского заказа
        :param length: Длинна.
        :param width: Ширина.
        :param height: Высота.
        :param delivery_point_code: Идентификатор точки доставки.
        :param pickup_time_period: Дата привоза на склад.
        :param date_pickup: Временной интервал.
        :param tariff: Тариф создания заказа.
        :param weight_1: Вес первого места в заказе.
        :param weight_2: Вес второго места в заказе.
        :param shop_number_1: Номер в магазине первого места в заказе.
        :param shop_number_2: Номер в магазине второго места в заказе.
        :param dimension: Габариты места заказа.
        """
        json_multi_order = json.dumps(
            {
                "warehouse": {
                    "id": str(self.database.metaship.get_list_warehouses()[0]),
                },
                "shop": {
                    "id": str(self.database.metaship.get_list_shops()[0]),
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
                    "email": "test@mail.ru",
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
        return self.app.http_method.post(link=self.link, data=json_multi_order)

    def post_import_order_format_russian_post(self, file_extension: str = None):
        r"""Метод создания заказа из файла XLSX или XLS формата.
        :param file_extension: Exel файл с расширением xlsx или xls.
        """
        file_xls = "orders_format_russian_post.xls"
        file_xlsx = "orders_format_russian_post.xlsx"
        json_order_from_file = {
            "shopId": str(self.database.metaship.get_list_shops()[0]),
            "warehouseId": str(self.database.metaship.get_list_warehouses()[0]),
            "type": "russian_post"
        }
        if file_extension == "xls":
            file = [("file", (f"{file_xls}", open(file=f"{self.directory}/{file_xls}", mode="rb"), self.method_xls))]
        elif file_extension == "xlsx":
            file = [("file", (f"{file_xlsx}", open(file=f"{self.directory}/{file_xlsx}", mode="rb"), self.method_xlsx))]
        else:
            return f"Файл {file_extension} не поддерживается"
        return self.app.http_method.post(link=f"import/{self.link}", data=json_order_from_file, files=file)

    def post_import_order(self, delivery_services: str = None, file_extension: str = None):
        r"""Метод создания заказа из файла XLSX или XLS формата.
        :param delivery_services: Служба доставки.
        :param file_extension: Exel файл с расширением xlsx или xls.
        """
        file_xls = f"orders_{delivery_services}.xls"
        file_xlsx = f"orders_{delivery_services}.xlsx"
        json_order_from_file = {
            "shopId": str(self.database.metaship.get_list_shops()[0]),
            "warehouseId": str(self.database.metaship.get_list_warehouses()[0]),
        }
        if file_extension == "xls":
            file = [("file", (f"{file_xls}", open(file=f"{self.directory}/{file_xls}", mode="rb"), self.method_xls))]
        elif file_extension == "xlsx":
            file = [("file", (f"{file_xlsx}", open(file=f"{self.directory}/{file_xlsx}", mode="rb"), self.method_xlsx))]
        else:
            return f"Файл {file_extension} не поддерживается"
        return self.app.http_method.post(link=f"import/{self.link}", data=json_order_from_file, files=file)

    def get_order_search(self, query: str):
        r"""Метод поиска по заказам.
        :param query: Метод поиска по ID, shop_number и тд.
        """
        search = {
            "query": query
        }
        return self.app.http_method.get(link=f"{self.link}/search", params=search)

    def get_orders(self):
        """Метод возвращает список заказов."""
        return self.app.http_method.get(link=self.link)

    def get_order_id(self, order_id: str, sec: float = 0):
        r"""Метод получения информации о заказе по его id.
        :param order_id: Идентификатор заказа.
        :param sec: Задержка перед методом для регистрации заказа в системе.
        """
        self.app.time_sleep(sec)
        return self.app.http_method.get(link=f"{self.link}/{order_id}")

    def put_order(self, order_id: str, weight: str, length: str, width: str, height: str, declared_value: str,
                  family_name: str):
        r"""Метод обновления заказа для СД RussianPost и LPost.
        :param order_id: Идентификатор заказа.
        :param weight: Общий вес заказа.
        :param length: Длинна.
        :param width: Ширина.
        :param height: Высота.
        :param declared_value: Объявленная стоимость.
        :param family_name: ФИО получателя.
        """
        result_get_order_by_id = self.get_order_id(order_id=order_id)
        body_order = result_get_order_by_id.json()["data"]["request"]
        body_order["weight"] = weight
        body_order["dimension"]["length"] = length
        body_order["dimension"]["width"] = width
        body_order["dimension"]["height"] = height
        body_order["payment"]["declaredValue"] = declared_value
        body_order["recipient"]["familyName"] = family_name
        body = json.dumps(body_order)
        return self.app.http_method.put(link=f"{self.link}/{order_id}", data=body)

    def patch_order(self, order_id: str, name: str = None, price: float = None, count: int = None, weight: float = None,
                    path: str = None):
        r"""Метод редактирования поля в заказе.
        :param order_id: Идентификатор заказа.
        :param path: Наименования поля которое будем менять
        :param name: Наименование товарной позиции.
        :param price: Цена товарной позиции.
        :param count: Количество штук.
        :param weight: Вес товарной позиции.
        """
        if path == "weight":
            json_patch_order = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "weight",
                        "value": weight
                    }
                ]
            )
        else:
            json_patch_order = json.dumps(
                [
                    {
                        "op": "replace",
                        "path": "places",
                        "value": [
                            {
                                "items": [
                                    {
                                        "article": f"ART1{randrange(1000000, 9999999)}",
                                        "name": name,
                                        "price": price,
                                        "count": count,
                                        "weight": weight,
                                        "vat": "0"
                                    },
                                ],
                                "barcode": f"Box_2{randrange(100000, 999999)}",
                                "weight": 1,
                                "dimension": {
                                    "length": 10,
                                    "width": 10,
                                    "height": 10
                                }
                            }
                        ]
                    }
                ]
            )
        return self.app.http_method.patch(link=f"{self.link}/{order_id}", data=json_patch_order)

    def patch_order_add_item(self, order_id: str, path: str = None, shop_number_3: str = f"{randrange(100000, 999999)}",
                             weight_3: float = randint(1, 5), weight_4: float = randint(1, 5), dimension: dict = None):
        r"""Метод добавление места в заказ.
        :param order_id: Идентификатор заказа.
        :param path: Добавления items.
        :param shop_number_3: Номер нового items в магазине - значение по умолчанию, можно передать своё.
        :param weight_3: Вес нового items значение по умолчанию, можно передать своё.
        :param weight_4: Вес нового грузо места значение по умолчанию, можно передать своё (Для СД Cse).
        :param dimension: Габариты нового грузо места значение по умолчанию, можно передать своё (Для СД Cse).
        """
        result_get_order_by_id = self.get_order_id(order_id=order_id)
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
        return self.app.http_method.patch(link=f"{self.link}/{order_id}", data=json_path_order)

    def delete_order(self, order_id: str):
        r"""Метод удаления заказа.
        :param order_id: Идентификатор заказа.
        """
        return self.app.http_method.delete(link=f"{self.link}/{order_id}")

    def get_order_patches(self, order_id: str):
        r"""Метод получение PATCH изменений по заказу.
        :param order_id: Идентификатор заказа.
        """
        return self.app.http_method.get(link=f"{self.link}/{order_id}/patches")

    def get_order_statuses(self, order_id: str):
        r"""Метод получение информации об истории изменения статусов заказа.
        :param order_id: Идентификатор заказа.
        """
        return self.app.http_method.get(link=f"{self.link}/{order_id}/statuses")

    def get_order_details(self, order_id: str):
        r"""Метод получение подробной информации о заказе.
        :param order_id: Идентификатор заказа.
        """
        return self.app.http_method.get(link=f"{self.link}/{order_id}/details")

    def getting_all_order_id_out_parcel(self):
        """Метод получения id всех заказов не в партии."""
        list_orders_id = []
        order_list = self.get_orders()
        for order in order_list.json():
            if order["status"] == "created":
                list_orders_id.append(order["id"])
        return list_orders_id

    def getting_single_order_id_out_parcel(self):
        """Метод получения id одноместных заказов не в партии"""
        list_orders_id = []
        list_orders = self.get_orders()
        for order in list_orders.json():
            if order["status"] == "created" and len(order["data"]["request"]["places"]) == 1:
                list_orders_id.append(order["id"])
        return list_orders_id

    def getting_multi_order_id_out_parcel(self):
        """Метод получения id многоместных заказов не в партии"""
        list_orders_id = []
        list_orders = self.get_orders()
        for order in list_orders.json():
            if order["status"] == "created" and len(order["data"]["request"]["places"]) > 1:
                list_orders_id.append(order["id"])
        return list_orders_id

    def getting_single_order_in_parcel(self):
        """Метод получения id одноместных заказов в партии"""
        list_orders_id = []
        list_orders = self.get_orders()
        for order in list_orders.json():
            if order["status"] == "wait-delivery" and len(order["data"]["request"]["places"]) == 1:
                list_orders_id.append(order["id"])
        return list_orders_id

    def getting_all_order_in_parcel(self):
        """Метод получения id всех заказов не в партии."""
        list_orders_id = []
        order_list = self.get_orders()
        for order in order_list.json():
            if order["status"] == "wait-delivery":
                list_orders_id.append(order["id"])
        return list_orders_id
