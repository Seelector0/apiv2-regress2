from utils.json_fixture import DICT_OBJECT
from fixture.database import DataBase
from environment import ENV_OBJECT
import requests.exceptions
import simplejson.errors

import allure


class ApiIntakes:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())
        self.link = "intakes"

    def post_intakes(self, delivery_service):
        r"""Метод создание забора.
        :param delivery_service: СД только Boxberry, Cdek, Cse.
        """
        intakes = DICT_OBJECT.form_intakes(delivery_service=delivery_service)
        result = self.app.http_method.post(link=self.link, data=intakes)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_intakes(self):
        """Получение списка заборов."""
        result = self.app.http_method.get(link=self.link)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_intakes_id(self, intakes_id: str):
        r"""Получения информации о заборе по его id.
        :param intakes_id: Идентификатор забора.
        """
        result = self.app.http_method.get(link=f"{self.link}/{intakes_id}")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")
