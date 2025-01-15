from utils.global_enums import INFO
from utils.environment import ENV_OBJECT
from random import randrange, randint, choice, random
import datetime
import allure
import uuid
import random


class Dicts:

    def __init__(self, app):
        self.app = app

    @staticmethod
    def form_authorization(admin: bool = None):
        r"""Форма для создания токена.
        :param admin: Для использования admin api.
        """
        body_authorization = dict(grant_type="client_credentials")
        body_authorization["client_id"] = ENV_OBJECT.client_id()
        body_authorization["client_secret"] = ENV_OBJECT.client_secret()
        if admin:
            body_authorization["client_id"] = ENV_OBJECT.admin_id()
            body_authorization["client_secret"] = ENV_OBJECT.admin_secret()
            body_authorization["scope"] = "admin"
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
    def form_patch_body_warehouses_all():
        """Форма для редактирования всех полей склада."""
        return [
            {
                "op": "replace",
                "path": "contact.fullName",
                "value": "Гадя Петрович Хренова"
            },
            {
                "op": "replace",
                "path": "contact.phone",
                "value": "+79095630011"
            },
            {
                "op": "replace",
                "path": "contact.email",
                "value": "cool_email@ya.ru"
            },
            {
                "op": "replace",
                "path": "lPostWarehouseId",
                "value": "123456"
            },
            {
                "op": "replace",
                "path": "yandexWarehouseId",
                "value": "4eb18cc4-329d-424d-a8a8-abfd8926463d"
            },
            {
                "op": "replace",
                "path": "visibility",
                "value": False
            },
            {
                "op": "replace",
                "path": "dpdPickupNum",
                "value": "92929200"
            },
            {
                "op": "replace",
                "path": "pickup",
                "value": False
            },
            {
                "op": "replace",
                "path": "comment",
                "value": "здесь могла быть ваша реклама"
            },
            {
                "op": "replace",
                "path": "workingTime",
                "value": {
                    "timezone": "+03:00",
                    "monday": {
                        "from": "09:00",
                        "to": "18:00"
                    },
                    "tuesday": {
                        "from": "09:00",
                        "to": "18:00"
                    },
                    "wednesday": {
                        "from": "09:00",
                        "to": "18:00"
                    },
                    "thursday": {
                        "from": "09:00",
                        "to": "18:00"
                    },
                    "friday": {
                        "from": "09:00",
                        "to": "18:00"
                    },
                    "saturday": {
                        "from": "09:00",
                        "to": "18:00"
                    },
                    "sunday": {
                        "from": "09:00",
                        "to": "18:00"
                    }
                }
            }
        ]

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
    def form_warehouse_body(country_code: str = None, pickup: bool = True):
        r"""Форма для создания склада.
        :param country_code: Код страны склада.
        :param pickup: Осуществляется ли забор с данного склада.
        """
        address_raw = "115035, г Москва, р-н Замоскворечье, ул Садовническая, д 14 стр 2"
        if country_code == "KZ":
            address_raw = "Алматы, микрорайон 10а, 13"
        return {
            "name": f"{randrange(100000, 999999)}",
            "address": {
                "raw": address_raw,
                "countryCode": country_code
            },
            "lPostWarehouseId": "20537",
            "yandexWarehouseId": "fbed3aa1-2cc6-4370-ab4d-59c5cc9bb924",
            "pickup": pickup,
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

    def form_info_body(self, shop_id, delivery_service_code: str, data: str = f"{datetime.date.today()}"):
        r"""Форма для Info methods.
          :param shop_id: Id магазина.
        :param delivery_service_code: Код СД.
        :param data: Желаемая дата доставки.
        """
        body_info = self.form_delivery_service_code(delivery_service_code=delivery_service_code)
        body_info["shopId"] = shop_id
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
            body_connection_type["data"] = dict(type="aggregation")
        return body_connection_type

    @staticmethod
    def form_offers(shop_id, warehouse_id, types: str, country_code: str = None):
        r"""Форма для получения офферов.
        :param shop_id: Идентификатор магазина.
        :param warehouse_id: Идентификатор склада.
        :param types: Параметр получения офферов.
        :param country_code: Код страны назначения.
        """
        address = "г Москва, пр-кт Мира, д 45 стр 2"
        if country_code == "KZ":
            address = "Астана, Сарыарка, улица Өрнек, строение 1/1 блок 1"
        return {
            "warehouseId": warehouse_id,
            "shopId": shop_id,
            "address": address,
            "declaredValue": randrange(1000, 5000),
            "length": randrange(1, 35),
            "width": randrange(1, 35),
            "height": randrange(1, 35),
            "weight": randrange(1, 10),
            "types[0]": types,
            "countryCode": country_code
        }

    @staticmethod
    def form_order(shop_id, warehouse_id, payment_type: str, declared_value: float, delivery_sum: float,  cod: float,
                   dimension: dict,  weight:  float, delivery_type: str, service: str, tariff: str,
                   delivery_point_code: str,  data: str, delivery_time: dict, pickup_time_period: str, date_pickup: str,
                   second_name: str = None, comment: str = None, email: str = None, shop_barcode: str = None,
                   country_code: str = None, type_order: str = None, intake_point_code: str = None):
        r"""Форма для создания заказов.
        :param shop_id: Id магазина.
        :param shop_barcode: Штрих код заказа.
        :param warehouse_id: Id склада.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param declared_value: Объявленная стоимость.
        :param delivery_sum: Стоимость доставки.
        :param cod: Наложенный платеж, руб.
        :param dimension: Габариты заказа.
        :param weight: Общий все заказа.
        :param delivery_type: Тип доставки 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param service: Код СД.
        :param tariff: Тариф создания заказа.
        :param delivery_point_code: Идентификатор точки доставки.
        :param data: Дата доставки.
        :param delivery_time: Если указанна поле 'data', то delivery_time обязателен для курьерского заказа
        :param country_code: Код страны назначения.
        :param pickup_time_period: Дата привоза на склад.
        :param date_pickup: Временной интервал.
        :param second_name: Отчество получателя.
        :param email: Электронная почта получателя.
        :param comment: Комментарий к заказу.
        :param type_order: Тип заказа.
        :param intake_point_code: Идентификатор точки сдачи возврата.
        """
        address_raw = "129110, г Москва, Мещанский р-н, пр-кт Мира, д 33 к 1"
        if country_code == "KZ":
            address_raw = "Астана, Сарыарка, улица Өрнек, строение 1/1 блок 1"
        return {
            "warehouse": {
                "id": warehouse_id,
            },
            "shop": {
                "id": shop_id,
                "number": f"{randrange(1000000, 9999999)}",
                "barcode": shop_barcode,
            },
            "payment": {
                "type": payment_type,
                "declaredValue": declared_value,
                "deliverySum": delivery_sum,
                "cod": cod
            },
            "dimension": dimension,
            "weight": weight,
            "delivery": {
                "type": delivery_type,
                "service": service,
                "tariff": tariff,
                "date": data,
                "time": delivery_time,
                "deliveryPointCode": delivery_point_code,
                "intakePointCode": intake_point_code,
            },
            "recipient": {
                "familyName": "Филипенко",
                "firstName": "Юрий",
                "secondName": second_name,
                "email": email,
                "phoneNumber": f"+7909{randrange(1000000, 9999999)}",
                "address": {
                    "raw": address_raw,
                    "countryCode": country_code,
                }
            },
            "type": type_order,
            "comment": comment,
            "pickupTimePeriod": pickup_time_period,
            "datePickup": date_pickup
        }

    @staticmethod
    def form_cargo_items(items: dict, barcode: str = None, shop_number: str = None, dimension: dict = None,
                         weight: str = None):
        r"""Форма для создания грузоместа.
        :param items: Товарная позиция.
        :param barcode: Штрихкод грузоместа.
        :param shop_number: Номер грузоместа.
        :param dimension: Габариты грузоместа.
        :param weight: Вес грузоместа.
        """
        return {
            "items": [
                items
            ],
            "barcode": barcode,
            "shopNumber": shop_number,
            "weight": weight,
            "dimension": dimension
        }

    @staticmethod
    def form_order_from_file(shop_id, warehouse_id, type_: str = None):
        r"""Форма для создания заказа из файла.
        :param shop_id: Id магазина.
        :param warehouse_id: Id склада.
        :param type_: Параметр для создания заказа из файла формата СД RussianPost.
        """
        body_order = {
            "shopId": shop_id,
            "warehouseId": warehouse_id
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

    def form_intakes(self, shop_id, warehouse_id, delivery_service: str):
        r"""Форма для создания забора.
        :param shop_id: Id магазина.
        :param warehouse_id: Id склада.
        :param delivery_service: Код СД.
        """
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        return {
            "deliveryService": delivery_service,
            "date": str(tomorrow),
            "shop": {
                "id": shop_id,
                "number": f"intake{randrange(1000000, 9999999)}"
            },
            "comment": "Позвонить за 3 часа до забора!",
            "from": {
                "warehouseId": warehouse_id
            },
            "to": {
                "warehouseId": warehouse_id
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

    # Убрал так как не используется в тестах, но грузит подключение к бд
    # def form_reports(self):
    #     """Форма для создания отчёта по заказам."""
    #     return {
    #         "filter": {
    #             "created": {
    #                 "dateTime": {
    #                     "from": "2020-07-20 13:00:00",
    #                     "to": "2020-07-20 14:00:00"
    #                 }
    #             },
    #             "shops": [
    #                 {
    #                     "id": self.connections.get_list_shops()[0]
    #                 }
    #             ],
    #             "parcels": [
    #                 {
    #                     "id": self.connections.get_list_parcels()[0]
    #                 }
    #             ]
    #         }
    #     }

    @staticmethod
    def places(places: list):
        r"""Создание в заказе мест.
        :param places: Места.
        """
        return [dict(items=places)]

    @staticmethod
    def items(name, price: float = 1000, count: int = randint(1, 3), weight: float = randint(1, 5), vat: str = "0",
              items_declared_value: int = 1000):
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
    def dimension(length: float = None, width: float = None, height: float = None):
        r"""Габариты товара или грузоместа.
        :param length: Длина. Если None, генерируется случайное значение.
        :param width: Ширина. Если None, генерируется случайное значение.
        :param height: Высота. Если None, генерируется случайное значение.
        """
        length = length if length is not None else random.randint(5, 30)
        width = width if width is not None else random.randint(5, 30)
        height = height if height is not None else random.randint(5, 30)

        return {'length': length, 'width': width, 'height': height}

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

    @staticmethod
    def settings_tariffs(tariffs):
        r"""Форма для изменения тарифов СД.
        :param tariffs: Тарифы СД.
        :return:
        """
        return dict(exclude=tariffs, restrict=None)

    @staticmethod
    def generate_random_number():
        r"""Генерация случайного числа для использования в номерах магазина или штрихкодах.
        :return: Случайное 7-значное число в виде строки.
        """
        random_number = f"{randrange(1000000, 9999999)}"
        return random_number
