from utils.checking import Checking
from utils.global_enums import INFO
import allure

    
class TestsWebHook:

    def __init__(self, app):
        self.app = app
        # self.db_connections = DataBaseConnections()

    @allure.description("Создание веб-хука")
    def post_webhook(self, shop_id: str):
        webhooks = self.app.webhook.post_webhook(shop_id=shop_id)
        Checking.check_status_code(response=webhooks, expected_status_code=200)
        Checking.checking_json_key(response=webhooks, expected_value=INFO.entity_webhook)

    @allure.description("Получение списка веб-хуков")
    def get_webhooks(self):
        list_webhooks = self.app.webhook.get_webhooks()
        Checking.check_status_code(response=list_webhooks, expected_status_code=200)
        Checking.check_response_is_not_empty(response=list_webhooks)

    # В тестах не используется, но грузит подключение к БД db_connections, если будут добавлены тесты вернуть
    # @allure.description("Получение веб-хука по его Id")
    # def get_webhook_by_id(self):
    #     random_webhook_id = choice(self.db_connections.get_list_webhook())
    #     webhook_id = self.app.webhook.get_webhook_id(webhook_id=random_webhook_id)
    #     Checking.check_status_code(response=webhook_id, expected_status_code=200)
    #     Checking.checking_json_key(response=webhook_id, expected_value=INFO.entity_webhook)
