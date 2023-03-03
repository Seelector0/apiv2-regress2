import json


class ApiWidget:

    def __init__(self, app):
        self.app = app

    def create_widget_tokens(self, shop_id: str):
        """Создание токена для виджета"""
        body = json.dumps(
            {
                "shopId": shop_id
            }
        )
        result_widget_tokens = self.app.http_method.post(link="/widgets/tokens", data=body)
        return result_widget_tokens

    def get_widget_tokens(self):
        """Получение списка токенов"""
        result_widget_tokens = self.app.http_method.get(link="/widgets/tokens")
        return result_widget_tokens

    def get_widget_tokens_by_id(self, widget_id: str):
        """Получение виджета"""
        result_widget_tokens_by_id = self.app.http_method.get(link=f"/widgets/tokens/{widget_id}")
        return result_widget_tokens_by_id
