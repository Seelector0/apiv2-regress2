from fixture.database import DataBase
from environment import ENV_OBJECT
import simplejson.errors
import allure


class ApiWebhook:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())
        self.link = "webhook"

    def post_webhook(self, shop_id):
        """Метод создание веб-хука."""
        webhook = {
            "shopId": shop_id,
            "url": "https://develop.mock.metaship.ppdev.ru/castlemock/mock/rest/project/gCaSpB/application/JYW0LQ/ok",
            "name": "Подписка на обновление статусов",
            "eventType": "StatusUpdate",
            "secret": "string"
        }
        result = self.app.http_method.post(link=self.link, data=webhook)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_webhooks(self):
        """Получение списка веб-хуков."""
        result = self.app.http_method.get(link=self.link)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_webhook_id(self, webhook_id: str):
        r"""Получение веб-хука по его id.
        :param webhook_id: Идентификатор веб-хука.
        """
        result = self.app.http_method.get(link=f"{self.link}/{webhook_id}")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def webhook_to_change_order_status(self, url: str):
        r"""Веб-хук на смену статуса заказа.
        :param url: URL веб-хука.
        """
        change_order_status = {
            "shopId": self.database.metaship.get_list_shops()[0],
            "url": "https://test.test/test",
            "name": "Подписка на обновление статусов",
            "eventType": "StatusUpdate",
            "secret": "string"
        }
        result = self.app.http_method.post(link=f"{url}", data=change_order_status)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")
