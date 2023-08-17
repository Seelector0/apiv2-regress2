from fixture.database import DataBase
from environment import ENV_OBJECT
from random import randrange, randint
import datetime


class Dict:

    def __init__(self):
        self.database_connections = DataBase(database=ENV_OBJECT.db_connections())
        self.database_customer = DataBase(database=ENV_OBJECT.db_customer_api())

    @staticmethod
    def form_token(client_id: str, client_secret: str):
        r"""Тело для создания токена.
        :param client_id: Токен.
        :param client_secret: Секретный код.
        """
        token = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        return token

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
        warehouse_body = {
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
        return warehouse_body

    @staticmethod
    def form_connection_type(delivery_service_code: str, aggregation: bool = None):
        r"""Тело для подключения СД.
        :param delivery_service_code: Название СД.
        :param aggregation: Признак того, что настройка выполнена или выполняется на агрегацию.
        """
        body_connection_type = {
            "deliveryServiceCode": delivery_service_code,
            "data": {
            }
        }
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
            "customerId": f"{ENV_OBJECT.customer_id()}",
            "connectionId": f"{self.database_customer.customer.get_connections_id(shop_id=shop_id)[0]}",
            "agreementId": "19852a56-8e10-4516-8218-8acefc2c2bd2",
            "customerAgreementId": f"{ENV_OBJECT.customer_agreements_id()}",
            "credential": {
            },
            "deliveryService": delivery_service_code
        }
        return body_connection

    def form_order(self, payment_type: str, declared_value: float, type_ds: str, service: str, barcode: str = None,
                   cod: float = None, length: float = randint(10, 30), width: float = randint(10, 50),
                   height: float = randint(10, 50), weight: float = randint(1, 5), tariff: str = None,
                   delivery_sum: float = None, data: str = None, delivery_time: dict = None,
                   delivery_point_code: str = None,  pickup_time_period: str = None, date_pickup: str = None,
                   routes: list = None,):
        r"""Тело для создания заказов.
        :param barcode: Штрих код заказа.
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
        order_body = {
            "warehouse": {
                "id": str(self.database_connections.metaship.get_list_warehouses()[0]),
            },
            "shop": {
                "id": str(self.database_connections.metaship.get_list_shops()[0]),
                "number": f"{randrange(1000000, 9999999)}",
                "barcode": barcode,
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
        return order_body

    def order_from_file(self, type_: str = None):
        r"""Тело для создания заказа из файла.
        :param type_: Параметр для создания заказа из файла формата СД RussianPost.
        """
        order_body = {
            "shopId": str(self.database_connections.metaship.get_list_shops()[0]),
            "warehouseId": str(self.database_connections.metaship.get_list_warehouses()[0])
        }
        if type_:
            order_body["type"] = type_
        return order_body

    @staticmethod
    def form_parcel_body(orders_ids, data: str):
        """Тело для создания партии."""
        parcel_body = {
            "orderIds": orders_ids,
            "shipmentDate": data
        }
        return parcel_body

    def form_intakes(self, delivery_service: str):
        """Тело для создания забора."""
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        intakes_body = {
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
        return intakes_body

    @staticmethod
    def form_patch_body(op: str, path: str, value):
        r"""Тело для редактирования полей.
        :param op: Тип операции.
        :param path: Изменяемое поле.
        :param value: Значение.
        """
        patch_body = [
            {
                "op": op,
                "path": path,
                "value": value
            }
        ]
        return patch_body


DICT_OBJECT = Dict()
