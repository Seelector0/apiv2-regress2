import json


class ApiWebhook:

    def __init__(self, app):
        self.app = app

    def create_webhook(self, shop_id, headers):
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
        result_webhook = self.app.http_method.post(link="/webhook", data=json_webhook, headers=headers)
        return result_webhook

    def get_webhooks(self, headers):
        """Получение списка веб-хуков"""
        result_get_webhooks = self.app.http_method.get(link="/webhook", headers=headers)
        return result_get_webhooks

    def get_webhook_by_id(self, webhook_id, headers):
        """Получение веб-хука по его id"""
        result_get_webhook_by_id = self.app.http_method.get(link=f"/webhook/{webhook_id}", headers=headers)
        return result_get_webhook_by_id

    def webhook_to_change_order_status(self, url, shop_id, headers):
        """Веб-хук на смену статуса заказа"""
        json_change_order_status = json.dumps(
            {
                "shopId": shop_id,
                "url": "https://test.test/test",
                "name": "Подписка на обновление статусов",
                "eventType": "StatusUpdate",
                "secret": "string"
            }
        )
        result_webhook_to_change_order_status = self.app.http_method.post(link=f"/{url}", data=json_change_order_status,
                                                                          headers=headers)
        return result_webhook_to_change_order_status
