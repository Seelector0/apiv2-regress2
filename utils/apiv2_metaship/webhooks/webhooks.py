from fixture.database import DataBase
from environment import ENV_OBJECT
import requests.exceptions
import simplejson.errors
import allure


class ApiWebhook:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())
        self.link = "webhook"

    def post_webhook(self, shop_id: str):
        """Метод создания веб-хука."""
        webhook = self.app.dict.form_webhook(shop_id=shop_id)
        result = self.app.http_method.post(link=self.link, json=webhook)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_webhooks(self):
        """Получение списка веб-хуков."""
        result = self.app.http_method.get(link=self.link)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_webhook_id(self, webhook_id: str):
        r"""Получение веб-хука по его id.
        :param webhook_id: Идентификатор веб-хука.
        """
        result = self.app.http_method.get(link=f"{self.link}/{webhook_id}")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")
