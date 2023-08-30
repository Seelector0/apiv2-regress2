

class ApiWidget:

    def __init__(self, app):
        self.app = app
        self.link = "widget/tokens"

    def post_widget_tokens(self, shop_id: str):
        r"""Создание токена для виджета.
        :param shop_id: Id магазина из БД.
        """
        widget = self.app.dict.form_widget(shop_id=shop_id)
        result = self.app.http_method.post(link=self.link, json=widget)
        return self.app.http_method.return_result(response=result)

    def get_widget_tokens(self):
        """Получение списка токенов."""
        result = self.app.http_method.get(link=self.link)
        return self.app.http_method.return_result(response=result)

    def get_widget_tokens_id(self, widget_id: str):
        r"""Получение виджета.
        :param widget_id: Идентификатор виджета.
        """
        result = self.app.http_method.get(link=f"{self.link}/{widget_id}")
        return self.app.http_method.return_result(response=result)
