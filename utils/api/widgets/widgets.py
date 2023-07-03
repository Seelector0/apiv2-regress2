from fixture.database import DataBase
from environment import ENV_OBJECT
import json


class ApiWidget:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())
        self.link = "widget/tokens"

    def post_widget_tokens(self):
        """Создание токена для виджета."""
        body = {
            "shopId": self.database.metaship.get_list_shops()[0]
        }
        return self.app.http_method.post(link=self.link, data=json.dumps(body))

    def get_widget_tokens(self):
        """Получение списка токенов."""
        return self.app.http_method.get(link=self.link)

    def get_widget_tokens_id(self, widget_id: str):
        r"""Получение виджета.
        :param widget_id: Идентификатор виджета.
        """
        return self.app.http_method.get(link=f"{self.link}/{widget_id}")
