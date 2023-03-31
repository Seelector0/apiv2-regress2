import json


class ApiWidget:

    def __init__(self, app):
        self.app = app
        self.link = "/widgets/tokens"

    def create_widget_tokens(self):
        """Создание токена для виджета"""
        shop_id = self.app.shop.getting_list_shop_ids()
        body = json.dumps(
            {
                "shopId": shop_id[0]
            }
        )
        return self.app.http_method.post(link=self.link, data=body)

    def get_widget_tokens(self):
        """Получение списка токенов"""
        return self.app.http_method.get(link=self.link)

    def get_widget_tokens_id(self, widget_id: str):
        """Получение виджета"""
        return self.app.http_method.get(link=f"{self.link}/{widget_id}")
