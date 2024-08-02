

class Forms:

    def __init__(self, app):
        self.app = app
        self.link = "forms"

    def post_forms(self, parcel_id):
        """Создание формы с этикетками партии."""
        forms_url = f"{self.link}/{self.app.parcel.link}/{parcel_id}/labels"
        result = self.app.http_method.post(link=forms_url)
        return self.app.http_method.return_result(response=result)

    def get_forms(self):
        """Получения списка форм."""
        result = self.app.http_method.get(link=self.link)
        return self.app.http_method.return_result(response=result)

    def get_forms_id(self, forms_id):
        r"""Получение формы по идентификатору.
        :param forms_id: Id формы.
        """
        result = self.app.http_method.get(link=f"{self.link}/{forms_id}")
        return self.app.http_method.return_result(response=result)
