import json


class ApiWebhook:

    def __init__(self, app):
        self.app = app
        self.link = "/webhook"

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
        result_webhook = self.app.http_method.post(link=self.link, data=json_webhook)
        return result_webhook

    def get_webhooks(self):
        """Получение списка веб-хуков"""
        result_get_webhooks = self.app.http_method.get(link=self.link)
        return result_get_webhooks

    def get_webhook_by_id(self, webhook_id: str):
        """Получение веб-хука по его id"""
        result_get_webhook_by_id = self.app.http_method.get(link=f"{self.link}/{webhook_id}")
        return result_get_webhook_by_id

    def webhook_to_change_order_status(self, url: str):
        """Веб-хук на смену статуса заказа"""
        shop_id = self.app.shop.get_shops_id()
        json_change_order_status = json.dumps(
            {
                "shopId": shop_id[0],
                "url": "https://test.test/test",
                "name": "Подписка на обновление статусов",
                "eventType": "StatusUpdate",
                "secret": "string"
            }
        )
        result_webhook_to_change_order_status = self.app.http_method.post(link=f"/{url}", data=json_change_order_status)
        return result_webhook_to_change_order_status
