from fixture.database import DataBase
from environment import ENV_OBJECT
from random import randrange, randint
import datetime
import allure
import uuid


class Dict:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin
        self.database_connections = DataBase(database=ENV_OBJECT.db_connections())
        self.database_customer = DataBase(database=ENV_OBJECT.db_customer_api())

    @staticmethod
    def form_authorization(client_id: str, client_secret: str, admin: bool = None):
        r"""Тело для создания токена.
        :param client_id: Токен.
        :param client_secret: Секретный код.
        :param admin: Для использования admin api.
        """
        body_authorization = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if admin is True:
            body_authorization["scope"] = "admin"
        return body_authorization

    @staticmethod
    def form_headers():
        """Тело headers."""
        body_headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        return body_headers

    @staticmethod
    def form_token(authorization: str):
        r"""Тело для получения токена.
        :param authorization:
        """
        x_trace_id = str(uuid.uuid4())
        with allure.step(title=f"x-trace-id: {x_trace_id}"):
            body_token = {
                "x-trace-id": x_trace_id,
                "Authorization": authorization
            }
            return body_token

    @staticmethod
    def form_shop_body():
        """Тело для создания магазина."""
        shop_body = {
            "name": f"INT{randrange(100000, 999999)}",
            "uri": f"integration-shop{randrange(1000, 9999)}.ru",
            "phone": f"7916{randrange(1000000, 9999999)}",
            "sender": "Иванов Иван Иванович"
        }
        return shop_body

    @staticmethod
    def form_warehouse_body():
        """Тело для создания склада."""
        body_warehouse = {
            "name": f"{randrange(100000, 999999)}",
            "address": {
                "raw": "115035, г Москва, р-н Замоскворечье, ул Садовническая, д 14 стр 2"
            },
            "lPostWarehouseId": "20537",
            "yandexWarehouseId": None,
            "pickup": True,
            "contact": {
                "fullName": "Виктор Викторович",
                "phone": f"+7910{randrange(1000000, 9999999)}",
                "email": "test@email.ru"
            }
        }
        return body_warehouse

    @staticmethod
    def form_delivery_service_code(delivery_service_code):
        r"""Тело СД.
        :param delivery_service_code: Код СД.
        """
        body_delivery_service_code = {
            "deliveryServiceCode": delivery_service_code
        }
        return body_delivery_service_code

    def form_info_body(self, delivery_service_code: str):
        """Тело для Info methods.
        :param delivery_service_code: Код СД.
        """
        body_info = Dict.form_delivery_service_code(delivery_service_code=delivery_service_code)
        body_info["shopId"] = self.database_connections.metaship.get_list_shops()[0]
        return body_info

    @staticmethod
    def form_connection_type(delivery_service_code: str, aggregation: bool = None):
        r"""Тело для подключения СД.
        :param delivery_service_code: Название СД.
        :param aggregation: Признак того, что настройка выполнена или выполняется на агрегацию.
        """
        body_connection_type = Dict.form_delivery_service_code(delivery_service_code=delivery_service_code)
        body_connection_type["data"]: dict = {}
        if aggregation is True:
            body_connection_type["data"]["type"] = "aggregation"
        return body_connection_type

    def form_moderation_delivery_services(self, delivery_service_code: str):
        r"""Тело для снятия с модерации СД.
        :param delivery_service_code: Название СД.
        """
        shop_id = self.database_connections.metaship.get_list_shops()[0]
        body_connection = {
            "shopId": shop_id,
            "customerId": ENV_OBJECT.customer_id(),
            "connectionId": self.database_customer.customer.get_connections_id(shop_id=shop_id)[0],
            "agreementId": "19852a56-8e10-4516-8218-8acefc2c2bd2",
            "customerAgreementId": ENV_OBJECT.customer_agreements_id(),
            "credential": {
            },
            "deliveryService": delivery_service_code
        }
        return body_connection

    def form_offers(self, types: str):
        """Тело для получения офферов"""
        body_offers = {
            "warehouseId": self.database_connections.metaship.get_list_warehouses()[0],
            "shopId": self.database_connections.metaship.get_list_shops()[0],
            "address": "г Москва, пр-кт Мира, д 45 стр 2",
            "declaredValue": randrange(1000, 5000),
            "height": randrange(10, 45),
            "length": randrange(10, 45),
            "width": randrange(10, 45),
            "weight": randrange(1, 10),
            "types[0]": types
        }
        return body_offers

    def form_order(self, payment_type: str, declared_value: float, type_ds: str, service: str, shop_barcode: str = None,
                   cod: float = None, length: float = randint(10, 30), width: float = randint(10, 50),
                   height: float = randint(10, 50), weight: float = randint(1, 5), tariff: str = None,
                   delivery_sum: float = None, data: str = None, delivery_time: dict = None,
                   delivery_point_code: str = None, pickup_time_period: str = None, date_pickup: str = None,
                   routes: list = None, ):
        r"""Тело для создания заказов.
        :param shop_barcode: Штрих код заказа.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param declared_value: Объявленная стоимость.
        :param delivery_sum: Стоимость доставки.
        :param cod: Наложенный платеж, руб.
        :param length: Длинна.
        :param width: Ширина.
        :param height: Высота.
        :param weight: Вес всего заказа.
        :param type_ds: Тип доставки 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param service: Код СД.
        :param tariff: Тариф создания заказа.
        :param data: Дата доставки.
        :param delivery_time: Если указанна поле 'data', то delivery_time обязателен для курьерского заказа
        :param delivery_point_code: Идентификатор точки доставки.
        :param pickup_time_period: Дата привоза на склад.
        :param date_pickup: Временной интервал.
        :param routes: Поле обязательное для создания заказа в СД DostavkaGuru.
        """
        body_order = {
            "warehouse": {
                "id": self.database_connections.metaship.get_list_warehouses()[0],
            },
            "shop": {
                "id": self.database_connections.metaship.get_list_shops()[0],
                "number": f"{randrange(1000000, 9999999)}",
                "barcode": shop_barcode,
            },
            "payment": {
                "type": payment_type,
                "declaredValue": declared_value,
                "deliverySum": delivery_sum,
                "cod": cod
            },
            "dimension": {
                "length": length,
                "width": width,
                "height": height
            },
            "weight": weight,
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
            "routes": routes
        }
        return body_order

    @staticmethod
    def form_cargo_items(items: dict, dimension: dict = None):
        r"""Тело для создания грузоместа.
        :param items: Товарная позиция.
        :param dimension: Габариты грузоместа.
        """
        body_cargo = {
            "items": [
                items
            ],
            "barcode": f"Box_3{randrange(100000, 999999)}",
            "shopNumber": f"{randrange(100000, 999999)}",
            "weight": randint(10, 30),
            "dimension": dimension
        }
        return body_cargo

    def form_order_from_file(self, type_: str = None):
        r"""Тело для создания заказа из файла.
        :param type_: Параметр для создания заказа из файла формата СД RussianPost.
        """
        body_order = {
            "shopId": self.database_connections.metaship.get_list_shops()[0],
            "warehouseId": self.database_connections.metaship.get_list_warehouses()[0]
        }
        if type_:
            body_order["type"] = type_
        return body_order

    @staticmethod
    def form_raw(raw: str):
        """Тело для разбора адреса.
        :param raw: Адрес.
        """
        body_raw = {
            "raw": raw
        }
        return body_raw

    @staticmethod
    def form_label(key: str, value):
        r"""Тело для получения этикеток.
        :param key: Название поля.
        :param value: Значения поля.
        """
        body_label = {
            f"{key}": value
        }
        return body_label

    @staticmethod
    def form_parcel_body(orders_ids, data: str):
        r"""Тело для создания партии.
        :param orders_ids: Список id заказов.
        :param data: Дата отгрузки партии.
        """
        body_parcel = {
            "orderIds": orders_ids,
            "shipmentDate": data
        }
        return body_parcel

    def form_intakes(self, delivery_service: str):
        r"""Тело для создания забора.
        :param delivery_service: Код СД.
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        body_intake = {
            "deliveryService": delivery_service,
            "date": str(tomorrow),
            "shop": {
                "id": self.database_connections.metaship.get_list_shops()[0],
                "number": f"intake{randrange(1000000, 9999999)}"
            },
            "comment": "Позвонить за 3 часа до забора!",
            "from": {
                "warehouseId": self.database_connections.metaship.get_list_warehouses()[0]
            },
            "to": {
                "warehouseId": self.database_connections.metaship.get_list_warehouses()[0]
            },
            "dimension": {
                "length": randint(10, 50),
                "width": randint(10, 50),
                "height": randint(10, 50)
            },
            "weight": randint(1, 5),
            "countCargoPlace": 1,
            "time": {
                "from": "12:00",
                "to": "15:00"
            },
            "description": "Классный груз"
        }
        return body_intake

    @staticmethod
    def form_widget(shop_id: str):
        body_widget = {
            "shopId": shop_id
        }
        return body_widget

    @staticmethod
    def form_webhook(shop_id: str):
        r"""Тело для создания веб-хука.
        :param shop_id: Идентификатор магазина.
        """
        body_webhook = {
            "shopId": shop_id,
            "url": "https://develop.mock.metaship.ppdev.ru/castlemock/mock/rest/project/gCaSpB/application/JYW0LQ/ok",
            "name": "Подписка на обновление статусов",
            "eventType": "StatusUpdate",
            "secret": "string"
        }
        return body_webhook

    @staticmethod
    def form_patch_body(op: str, path: str, value):
        r"""Тело для редактирования полей.
        :param op: Тип операции.
        :param path: Изменяемое поле.
        :param value: Значение.
        """
        body_patch = [
            {
                "op": op,
                "path": path,
                "value": value
            }
        ]
        return body_patch
