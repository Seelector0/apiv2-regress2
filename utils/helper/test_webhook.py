from utils.checking import Checking
from utils.response_schemas import SCHEMAS
import allure


class TestsWebHook:

    def __init__(self, app):
        self.app = app

    @allure.description("Создание веб-хука")
    def post_webhook(self, shop_id: str, shared_data):
        webhooks = self.app.webhook.post_webhook(shop_id=shop_id)
        Checking.check_status_code(response=webhooks, expected_status_code=200)
        Checking.check_json_schema(response=webhooks, schema=SCHEMAS.webhook.webhook_create_or_get_by_id)
        webhook_id = webhooks.json().get('id')
        shared_data["webhook_id"] = webhook_id

    @allure.description("Получение списка веб-хуков")
    def get_webhooks(self):
        list_webhooks = self.app.webhook.get_webhooks()
        Checking.check_status_code(response=list_webhooks, expected_status_code=200)
        Checking.check_response_is_not_empty(response=list_webhooks)
        Checking.check_json_schema(response=list_webhooks, schema=SCHEMAS.webhook.webhook_get)

    @allure.description("Получение веб-хука по его Id")
    def get_webhook_by_id(self, shared_data):
        webhook_id = self.app.webhook.get_webhook_id(webhook_id=shared_data["webhook_id"])
        Checking.check_status_code(response=webhook_id, expected_status_code=200)
        Checking.check_json_schema(response=webhook_id, schema=SCHEMAS.webhook.webhook_create_or_get_by_id)

    @allure.description("Удаление веб-хука")
    def delete_webhook(self, shared_data):
        webhook_id = self.app.webhook.delete_webhook(webhook_id=shared_data["webhook_id"])
        Checking.check_status_code(response=webhook_id, expected_status_code=204)
        response = self.app.webhook.get_webhook_id(webhook_id=shared_data["webhook_id"])
        Checking.check_status_code(response=response, expected_status_code=404)
