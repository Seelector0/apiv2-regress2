from fixture.database import DataBase
from environment import ENV_OBJECT
import allure


class ApiWidget:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())
        self.link = "widget/tokens"

    def post_widget_tokens(self, shop_id):
        """Создание токена для виджета."""
        body = {
            "shopId": shop_id
        }
        result = self.app.http_method.post(link=self.link, data=body)
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def get_widget_tokens(self):
        """Получение списка токенов."""
        result = self.app.http_method.get(link=self.link)
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def get_widget_tokens_id(self, widget_id: str):
        r"""Получение виджета.
        :param widget_id: Идентификатор виджета.
        """
        result = self.app.http_method.get(link=f"{self.link}/{widget_id}")
        with allure.step(title=f"Response: {result.json()}"):
            return result
