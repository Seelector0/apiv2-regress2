import json


class ApiWidget:

    def __init__(self, app):
        self.app = app
        self.link = "/widgets/tokens"

    def create_widget_tokens(self):
        """Создание токена для виджета"""
        shop_id = self.app.shop.get_shops_id()
        body = json.dumps(
            {
                "shopId": shop_id[0]
            }
        )
        result_widget_tokens = self.app.http_method.post(link=self.link, data=body)
        return result_widget_tokens

    def get_widget_tokens(self):
        """Получение списка токенов"""
        result_widget_tokens = self.app.http_method.get(link=self.link)
        return result_widget_tokens

    def get_widget_tokens_by_id(self, widget_id: str):
        """Получение виджета"""
        result_widget_tokens_by_id = self.app.http_method.get(link=f"{self.link}/{widget_id}")
        return result_widget_tokens_by_id
