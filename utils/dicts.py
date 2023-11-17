from databases.connections import DataBaseConnections
from databases.customer_api import DataBaseCustomerApi
from utils.global_enums import INFO
from environment import ENV_OBJECT
from random import randrange, randint, choice
import datetime
import allure
import uuid


class Dicts:

    def __init__(self, app, admin):
        self.app = app
        self.admin = admin
        self.db_connections = DataBaseConnections()
        self.db_customer_api = DataBaseCustomerApi()

    @staticmethod
    def form_authorization(admin: bool = None):
        r"""Форма для создания токена.
        :param admin: Для использования admin api.
        """
        body_authorization = dict(grant_type="client_credentials")
        if admin:
            body_authorization["client_id"] = ENV_OBJECT.admin_id()
            body_authorization["client_secret"] = ENV_OBJECT.admin_secret()
            body_authorization["scope"] = "admin"
        else:
            body_authorization["client_id"] = ENV_OBJECT.client_id()
            body_authorization["client_secret"] = ENV_OBJECT.client_secret()
        return body_authorization

    @staticmethod
    def form_headers():
        """Форма headers."""
        return {"Content-Type": "application/x-www-form-urlencoded"}

    @staticmethod
    def form_token(authorization: str):
        r"""Форма для получения токена.
        :param authorization: Токен для авторизации.
        """
        x_trace_id = str(uuid.uuid4())
        with allure.step(title=f"x-trace-id: {x_trace_id}"):
            body_token = dict(Authorization=f"Bearer {authorization}")
            body_token["x-trace-id"] = x_trace_id
            return body_token

    @staticmethod
    def form_patch_body(op: str, path: str, value: object):
        r"""Форма для редактирования полей.
        :param op: Тип операции.
        :param path: Изменяемое поле.
        :param value: Значение.
        """
        return [dict(op=op, path=path, value=value)]

    @staticmethod
    def form_shop_body():
        """Форма для создания магазина."""
        return {
            "name": f"INT{randrange(100000, 999999)}",
            "uri": f"integration-shop{randrange(1000, 9999)}.ru",
            "phone": f"7916{randrange(1000000, 9999999)}",
            "sender": "Иванов Иван Иванович"
        }

    @staticmethod
    def form_warehouse_body():
        """Форма для создания склада."""
        return {
            "name": f"{randrange(100000, 999999)}",
            "address": {
                "raw": "115035, г Москва, р-н Замоскворечье, ул Садовническая, д 14 стр 2"
            },
            "lPostWarehouseId": "20537",
            "yandexWarehouseId": "4eb18cc4-329d-424d-a8a8-abfd8926463d",
            "pickup": True,
            "contact": {
                "fullName": "Виктор Викторович",
                "phone": f"+7910{randrange(1000000, 9999999)}",
                "email": "test@email.ru"
            }
        }

    @staticmethod
    def form_delivery_service_code(delivery_service_code):
        r"""Форма СД.
        :param delivery_service_code: Код СД.
        """
        return dict(deliveryServiceCode=delivery_service_code)

    def form_info_body(self, delivery_service_code: str, data: str = f"{datetime.date.today()}"):
        r"""Форма для Info methods.
        :param delivery_service_code: Код СД.
        :param data: Желаемая дата доставки.
        """
        body_info = self.form_delivery_service_code(delivery_service_code=delivery_service_code)
        body_info["shopId"] = self.db_connections.get_list_shops()[0]
        body_info["deliveryDate"] = data
        return body_info

    def form_connection_type(self, delivery_service_code: str, aggregation: bool = None):
        r"""Форма для подключения СД.
        :param delivery_service_code: Название СД.
        :param aggregation: Признак того, что настройка выполнена или выполняется на агрегацию.
        """
        body_connection_type = self.form_delivery_service_code(delivery_service_code=delivery_service_code)
        body_connection_type["data"] = dict()
        if aggregation:
            body_connection_type["data"]["type"] = "aggregation"
        return body_connection_type

    def form_moderation_delivery_services(self, delivery_service_code: str):
        r"""Форма для снятия с модерации СД.
        :param delivery_service_code: Название СД.
        """
        shop_id = self.db_connections.get_list_shops()[0]
        return {
            "shopId": shop_id,
            "customerId": ENV_OBJECT.customer_id(),
            "connectionId": self.db_customer_api.get_connections_id(shop_id=shop_id)[0],
            "agreementId": "19852a56-8e10-4516-8218-8acefc2c2bd2",
            "customerAgreementId": ENV_OBJECT.customer_agreements_id(),
            "credential": dict(),
            "deliveryService": delivery_service_code
        }

    def form_offers(self, types: str):
        r"""Форма для получения офферов.
        :param types: Параметр получения оферов.
        """
        return {
            "warehouseId": self.db_connections.get_list_warehouses()[0],
            "shopId": self.db_connections.get_list_shops()[0],
            "address": "г Москва, пр-кт Мира, д 45 стр 2",
            "declaredValue": randrange(1000, 5000),
            "length": randrange(10, 45),
            "width": randrange(10, 45),
            "height": randrange(10, 45),
            "weight": randrange(1, 10),
            "types[0]": types
        }

    def form_order(self, payment_type: str, declared_value: float, type_ds: str, service: str, shop_barcode: str = None,
                   cod: float = None, length: float = randint(10, 30), width: float = randint(10, 50),
                   height: float = randint(10, 50), weight: float = randint(1, 5), tariff: str = None,
                   delivery_sum: float = None, data: str = None, delivery_time: dict = None,
                   delivery_point_code: str = None, pickup_time_period: str = None, date_pickup: str = None,
                   routes: list = None, ):
        r"""Форма для создания заказов.
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
        return {
            "warehouse": {
                "id": self.db_connections.get_list_warehouses()[0],
            },
            "shop": {
                "id": self.db_connections.get_list_shops()[0],
                "number": f"{randrange(1000000, 9999999)}",
                "barcode": shop_barcode,
            },
            "payment": {
                "type": payment_type,
                "declaredValue": declared_value,
                "deliverySum": delivery_sum,
                "cod": cod
            },
            "dimension": self.dimension(length=length, width=width, height=height),
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

    @staticmethod
    def form_cargo_items(items: dict, barcode: str = None, shop_number: str = None, dimension: dict = None):
        r"""Форма для создания грузоместа.
        :param items: Товарная позиция.
        :param barcode: Штрихкод грузоместа.
        :param shop_number: Номер грузоместа.
        :param dimension: Габариты грузоместа.
        """
        return {
            "items": [
                items
            ],
            "barcode": barcode,
            "shopNumber": shop_number,
            "weight": randint(1, 5),
            "dimension": dimension
        }

    def form_order_from_file(self, type_: str = None):
        r"""Форма для создания заказа из файла.
        :param type_: Параметр для создания заказа из файла формата СД RussianPost.
        """
        body_order = {
            "shopId": self.db_connections.get_list_shops()[0],
            "warehouseId": self.db_connections.get_list_warehouses()[0]
        }
        if type_:
            body_order["type"] = type_
        return body_order

    @staticmethod
    def form_parcel_body(orders_ids, data: str):
        r"""Форма для создания партии.
        :param orders_ids: Список id заказов.
        :param data: Дата отгрузки партии.
        """
        return dict(orderIds=orders_ids, shipmentDate=data)

    def form_intakes(self, delivery_service: str):
        r"""Форма для создания забора.
        :param delivery_service: Код СД.
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        return {
            "deliveryService": delivery_service,
            "date": str(tomorrow),
            "shop": {
                "id": self.db_connections.get_list_shops()[0],
                "number": f"intake{randrange(1000000, 9999999)}"
            },
            "comment": "Позвонить за 3 часа до забора!",
            "from": {
                "warehouseId": self.db_connections.get_list_warehouses()[0]
            },
            "to": {
                "warehouseId": self.db_connections.get_list_warehouses()[0]
            },
            "dimension": self.dimension(),
            "weight": randint(1, 5),
            "countCargoPlace": 1,
            "time": {
                "from": "12:00",
                "to": "15:00"
            },
            "description": "Классный груз"
        }

    @staticmethod
    def form_webhook(shop_id: str):
        r"""Форма для создания веб-хука.
        :param shop_id: Идентификатор магазина.
        """
        return {
            "shopId": shop_id,
            "url": "https://develop.mock.metaship.ppdev.ru/castlemock/mock/rest/project/gCaSpB/application/JYW0LQ/ok",
            "name": "Подписка на обновление статусов",
            "eventType": "StatusUpdate",
            "secret": "string"
        }

    def form_reports(self, data: str = datetime.date.today()):
        """Форма для создания отчёта по заказам."""
        return {
            "filter": {
                "created": {
                    "dateTime": {
                        "from": f"{data} 13:00:00",
                        "to": f"{data} 14:00:00"
                    }
                },
                "shops": [
                    {
                        "id": self.db_connections.get_list_shops()[0]
                    }
                ]
            }
        }

    def form_forms_labels(self):
        """Форма для создания формы с этикетками партии."""
        return {
            "id": "aaf1a0dd-3c6a-44eb-9bef-879eb5fd1963",
            "state": "ready",
            "message": "Невозможно создать этикетку",
            "type": "parcel_label",
            "data": {
                "filter": {
                    "parcels": [
                        {
                            "id": f"{self.db_connections.get_list_parcels()[0]}"
                        }
                    ]
                }
            },
            "artifacts": [
                {
                    "format": "link",
                    "data": "https://test.test/test.xlsx"
                }
            ],
            "createdAt": "2021-07-01T14:51:56+00:00",
            "stateTime": "2021-07-01T14:51:56+00:00"
        }

    @staticmethod
    def places(places: list):
        r"""Создание в заказе мест.
        :param places: Места.
        """
        return [dict(items=places)]

    @staticmethod
    def items(name, price: float = 1000, count: int = randint(1, 3), weight: float = randint(1, 5), vat: str = "0",
              items_declared_value: int = None):
        r"""Товарная позиция.
        :param name: Название товарной позиции.
        :param price: Цена товарной позиции
        :param count: Количество.
        :param weight: Вес товарной позиции.
        :param vat: Ставка НДС.
        :param items_declared_value: Цена одной товарной позиции.
        """
        return {
            "article": f"ART_{randrange(1000000, 9999999)}",
            "name": name,
            "price": price,
            "count": count,
            "weight": weight,
            "vat": vat,
            "declaredValue": items_declared_value,
        }

    @staticmethod
    def dimension(length: float = randint(10, 30), width: float = randint(10, 30), height: float = randint(10, 30)):
        r"""Габариты товара или грузоместа.
        :param length: Длинна.
        :param width: Ширина.
        :param height: Высота.
        """
        return dict(length=length, width=width, height=height)

    @staticmethod
    def recipient(family_name: str, first_name: str, second_name: str, phone_number: str, email: str, address: str):
        r"""Информация о получателе.
        :param family_name: Фамилия получателя.
        :param first_name: Имя получателя.
        :param second_name: Отчество получателя.
        :param phone_number: Контактный телефон получателя.
        :param email: Email получателя.
        :param address: Адрес получателя.
        """
        return {
            "familyName": family_name,
            "firstName": first_name,
            "secondName": second_name,
            "phoneNumber": phone_number,
            "email": email,
            "address": address
        }

    def replace_items_cdek(self, name):
        r"""Для редактирования товарных позиций для СД Cek.
        :param name: Наименование товара.
        """
        return {
            "barcode": f"{randrange(1000000, 9999999)}",
            "shopNumber": f"{randrange(1000000, 9999999)}",
            "weight": randint(1, 5),
            "dimension": self.dimension(),
            "items": [
                self.items(name=name, price=1000, count=randint(1, 3), weight=randint(1, 5),
                           vat=str(choice(INFO.cdek_vats)["code"]))
            ]
        }

    @staticmethod
    def delivery_interval(tariff: str, time_from: str, time_to: str):
        r"""Для редактирования времени доставки СД Cdek только курьер.
        :param tariff: Тариф заказа
        :param time_from: С какого часа доставка.
        :param time_to: По какой час доставка.
        :return:
        """
        return {
            "type": "Courier",
            "service": "Cdek",
            "tariff": tariff,
            "date": str(datetime.date.today()),
            "time": {
                "from": time_from,
                "to": time_to
            }
        }

# @allure.description("Изменение времени доставки заказа")
# def test_patch_delivery_intervals(app, connections):
#     order = list()
#     singles_orders_ids: list = connections.get_list_all_orders_out_parcel()
#     for single_order in singles_orders_ids:
#         orders = app.order.get_order_id(order_id=single_order)
#         if orders.json()["data"]["request"]["delivery"]["type"] == "Courier":
#             order.append(orders.json()["id"])
#     random_order_id = choice(order)
#     patch_order = app.order.patch_delivery_courier_cdek(order_id=random_order_id, time_from="10:00", time_to="14:00")
#     Checking.check_status_code(response=patch_order, expected_status_code=200)
#     Checking.checking_json_value(response=patch_order, key_name="status", expected_value="created")
#     Checking.checking_json_value(response=patch_order, key_name="state", expected_value="editing-external-processing")
#     connections.wait_create_order(order_id=random_order_id)
#     order_by_id = app.order.get_order_id(order_id=random_order_id)
#     Checking.check_status_code(response=order_by_id, expected_status_code=200)
#     Checking.checking_json_value(response=order_by_id, key_name="status", expected_value="created")
#     Checking.checking_json_value(response=order_by_id, key_name="state", expected_value="succeeded")
#     print(order_by_id.json()["id"])
#     print(order_by_id.json()["data"]["request"]["delivery"])
