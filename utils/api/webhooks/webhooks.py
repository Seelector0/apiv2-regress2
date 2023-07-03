from environment import ENV_OBJECT
from fixture.database import DataBase
import json


class ApiWebhook:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())
        self.link = "webhook"

    def create_webhook(self):
        """Создание веб-хука."""
        webhook = {
            "shopId": self.database.metaship.get_list_shops()[0],
            "url": "https://develop.mock.metaship.ppdev.ru/castlemock/mock/rest/project/gCaSpB/application/JYW0LQ/ok",
            "name": "Подписка на обновление статусов",
            "eventType": "StatusUpdate",
            "secret": "string"
        }
        return self.app.http_method.post(link=self.link, data=json.dumps(webhook))

    def get_webhooks(self):
        """Получение списка веб-хуков."""
        return self.app.http_method.get(link=self.link)

    def get_webhook_id(self, webhook_id: str):
        r"""Получение веб-хука по его id.
        :param webhook_id: Идентификатор веб-хука.
        """
        return self.app.http_method.get(link=f"{self.link}/{webhook_id}")

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
        return self.app.http_method.post(link=f"{url}", data=json.dumps(change_order_status))
