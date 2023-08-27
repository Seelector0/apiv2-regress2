from fixture.database import DataBase
from environment import ENV_OBJECT
import requests.exceptions
import simplejson.errors
import datetime
import allure


class ApiInfo:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())

    def delivery_time_schedules(self, delivery_service_code: str, postal_code: str = None, tariff_id: str = None):
        r"""Получение интервалов доставки конкретной СД.
        :param delivery_service_code: Код СД.
        :param postal_code: Индекс (только для СД TopDelivery).
        :param tariff_id: Атрибут указывающий тип доставки, в котором доступен интервал (только для СД Dalli).
        """
        params = self.app.dict.form_info_body(delivery_service_code=delivery_service_code)
        params["deliveryDate"] = f"{datetime.date.today()}"
        if postal_code:
            params["postalCode"] = postal_code
        elif tariff_id:
            params["tariffId"] = tariff_id
        else:
            params = self.app.dict.form_delivery_service_code(delivery_service_code=delivery_service_code)
        result = self.app.http_method.get(link="info/delivery_time_schedules", params=params)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def delivery_service_points(self, delivery_service_code: str, city_raw: str = "г. Москва"):
        r"""Получение списка ПВЗ конкретной СД.
        :param delivery_service_code: Код СД.
        :param city_raw: Адресная строка по умолчанию г. Москва.
        """
        params = self.app.dict.form_info_body(delivery_service_code=delivery_service_code)
        params["cityRaw"] = city_raw
        result = self.app.http_method.get(link="customer/info/delivery_service_points", params=params)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def info_vats(self, delivery_service_code: str):
        r"""Получение списка ставок НДС, которые умеет принимать и обрабатывать конкретная СД.
        :param delivery_service_code: Код СД.
        """
        params = self.app.dict.form_delivery_service_code(delivery_service_code=delivery_service_code)
        result = self.app.http_method.get(link="info/vats", params=params)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def intake_offices(self, delivery_service_code: str):
        r"""Получение списка точек сдачи.
        :param delivery_service_code: Код СД.
        """
        params = self.app.dict.form_delivery_service_code(delivery_service_code=delivery_service_code)
        result = self.app.http_method.get(link="info/intake_offices", params=params)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def info_statuses(self):
        """Получение полного актуального списка возможных статусов заказа."""
        result = self.app.http_method.get(link="info/statuses")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_tariffs(self, code):
        r"""Получение информации о тарифах поддерживаемых СД.
        :param code: Код СД.
        """
        result = self.app.http_method.get(link=f"info/{code}/tariffs")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def info_delivery_service_services(self, code: str):
        """Получение информации о дополнительных услугах поддерживаемых СД.
        :param code: Код СД.
        """
        result = self.app.http_method.get(link=f"info/delivery_service/{code}/services")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def user_clients(self):
        """Получение списка ключей."""
        result = self.app.http_method.get(link="user/clients")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def user_clients_id(self, user_id: str):
        r"""Получение информации о ключе подключения по id.
        :param user_id: Идентификатор клиента.
        """
        result = self.app.http_method.get(link=f"user/clients/{user_id}")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def info_address(self, raw: str = "101000, г Москва"):
        r"""Разбор адреса.
        :param raw: Адрес.
        """
        params = self.app.dict.form_raw(raw=raw)
        result = self.app.http_method.get(link="info/address", params=params)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")
