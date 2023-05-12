from fixture.database import DataBase
from environment import ENV_OBJECT
import datetime


class ApiInfo:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())

    def delivery_time_schedules(self, delivery_service_code: str, day: str = None):
        r"""Получение интервалов доставки конкретной СД.
        :param delivery_service_code: Код СД.
        :param day: Только для СД TopDelivery.
        """
        if day == "today":
            params = {
                "deliveryServiceCode": delivery_service_code,
                "deliveryDate": f"{datetime.date.today()}",
                "shopId": self.database.metaship.get_list_shops()[0],
                "postalCode": "101000"
            }
        else:
            params = {
                "deliveryServiceCode": delivery_service_code,
            }
        return self.app.http_method.get(link="info/delivery_time_schedules", params=params)

    def delivery_service_points(self, delivery_service_code: str, city_raw="г. Москва"):
        r"""Получение списка ПВЗ конкретной СД.
        :param delivery_service_code: Код СД.
        :param city_raw: Адресная строка по умолчанию г. Москва.
        """
        params = {
            "deliveryServiceCode": delivery_service_code,
            "shopId": self.database.metaship.get_list_shops()[0],
            "cityRaw": city_raw
        }
        return self.app.http_method.get(link="customer/info/delivery_service_points", params=params)

    def info_vats(self, delivery_service_code: str):
        r"""Получение списка ставок НДС, которые умеет принимать и обрабатывать конкретная СД.
        :param delivery_service_code: Код СД.
        """
        params = {
            "deliveryServiceCode": delivery_service_code
        }
        return self.app.http_method.get(link="info/vats", params=params)

    def intake_offices(self, delivery_service_code: str):
        r"""Получение списка точек сдачи.
        :param delivery_service_code: Код СД.
        """
        params = {
            "deliveryServiceCode": delivery_service_code
        }
        return self.app.http_method.get(link="info/intake_offices", params=params)

    def info_statuses(self):
        """Получение полного актуального списка возможных статусов заказа."""
        return self.app.http_method.get(link="/info/statuses")

    def info_delivery_service_services(self, code: str):
        """Получение информации о дополнительных услугах поддерживаемых СД.
        :param code: Код СД.
        """
        return self.app.http_method.get(link=f"info/delivery_service/{code}/services")

    def user_clients(self):
        """Получение списка ключей."""
        return self.app.http_method.get(link="user/clients")

    def user_clients_id(self, user_id: str):
        r"""Получение информации о ключе подключения по id.
        :param user_id: Идентификатор клиента.
        """
        return self.app.http_method.get(link=f"user/clients/{user_id}")

    def info_address(self, raw: str = "101000, г Москва"):
        r"""Разбор адреса.
        :param raw: Адрес.
        """
        params = {
            "raw": raw
        }
        return self.app.http_method.get(link="info/address", parsms=params)
