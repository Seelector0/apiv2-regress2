from fixture.database import DataBase
from environment import ENV_OBJECT
import requests.exceptions
import simplejson.errors
import allure


class ApiWidget:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())
        self.link = "widget/tokens"

    def post_widget_tokens(self, shop_id: str):
        r"""Создание токена для виджета.
        :param shop_id: Id магазина из БД.
        """
        body = {
            "shopId": shop_id
        }
        result = self.app.http_method.post(link=self.link, data=body)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_widget_tokens(self):
        """Получение списка токенов."""
        result = self.app.http_method.get(link=self.link)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_widget_tokens_id(self, widget_id: str):
        r"""Получение виджета.
        :param widget_id: Идентификатор виджета.
        """
        result = self.app.http_method.get(link=f"{self.link}/{widget_id}")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")
