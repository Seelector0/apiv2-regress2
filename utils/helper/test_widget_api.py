from databases.connections import DataBaseConnections
from databases.widget_api import DataBaseWidgetApi
from utils.global_enums import INFO
from utils.checking import Checking
from random import choice
import allure


class TestsWidget:

    def __init__(self, app):
        self.app = app
        self.db_connections = DataBaseConnections()
        self.db_widget_api = DataBaseWidgetApi()

    @allure.description("Создание токена для виджета")
    def post_token_for_widget(self, shop_id: str):
        token = self.app.widget.post_widget_tokens(shop_id=shop_id)
        Checking.check_status_code(response=token, expected_status_code=201)
        Checking.checking_json_key(response=token, expected_value=INFO.created_entity_widget)

    @allure.description("Получение списка токенов")
    def get_tokens(self):
        list_tokens = self.app.widget.get_widget_tokens()
        Checking.check_status_code(response=list_tokens, expected_status_code=200)
        Checking.check_response_is_not_empty(response=list_tokens)

    @allure.description("Получение токена по его Id")
    def get_token_by_id(self):
        widget_id = choice(self.db_widget_api.get_widgets_id(shop_id=self.db_connections.get_list_shops()[0]))
        token_id = self.app.widget.get_widget_tokens_id(widget_id=widget_id)
        Checking.check_status_code(response=token_id, expected_status_code=200)
        Checking.checking_json_key(response=token_id, expected_value=INFO.entity_widget)
