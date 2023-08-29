

class ApiWebhook:

    def __init__(self, app):
        self.app = app
        self.link = "webhook"

    def post_webhook(self, shop_id: str):
        """Метод создания веб-хука."""
        webhook = self.app.dict.form_webhook(shop_id=shop_id)
        result = self.app.http_method.post(link=self.link, json=webhook)
        return self.app.http_method.return_result(response=result)

    def get_webhooks(self):
        """Получение списка веб-хуков."""
        result = self.app.http_method.get(link=self.link)
        return self.app.http_method.return_result(response=result)

    def get_webhook_id(self, webhook_id: str):
        r"""Получение веб-хука по его id.
        :param webhook_id: Идентификатор веб-хука.
        """
        result = self.app.http_method.get(link=f"{self.link}/{webhook_id}")
        return self.app.http_method.return_result(response=result)
