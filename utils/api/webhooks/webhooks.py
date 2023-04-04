import json


class ApiWebhook:

    def __init__(self, app):
        self.app = app
        self.link = "webhook"

    def create_webhook(self, shop_id: str):
        """Создание веб-хука"""
        json_webhook = json.dumps(
            {
                "shopId": shop_id,
                "url": "https://develop.mock.metaship.ppdev.ru/castlemock/mock/rest/project/gCaSpB/application/JYW0LQ/ok",
                "name": "Подписка на обновление статусов",
                "eventType": "StatusUpdate",
                "secret": "string"
            }
        )
        return self.app.http_method.post(link=self.link, data=json_webhook)

    def get_webhooks(self):
        """Получение списка веб-хуков"""
        return self.app.http_method.get(link=self.link)

    def get_webhook_id(self, webhook_id: str):
        """Получение веб-хука по его id"""
        return self.app.http_method.get(link=f"{self.link}/{webhook_id}")

    def webhook_to_change_order_status(self, url: str):
        """Веб-хук на смену статуса заказа"""
        json_change_order_status = json.dumps(
            {
                "shopId": self.app.shop.getting_list_shop_ids()[0],
                "url": "https://test.test/test",
                "name": "Подписка на обновление статусов",
                "eventType": "StatusUpdate",
                "secret": "string"
            }
        )
        return self.app.http_method.post(link=f"{url}", data=json_change_order_status)
