

class ApiReports:

    def __init__(self, app):
        self.app = app
        self.link = "orders/report"

    def post_reports(self):
        """Метод для создания отчёта по заказам."""
        reports = self.app.dicts.form_reports()
        result = self.app.http_method.post(link=self.link, json=reports)
        return self.app.http_method.return_result(response=result)

    def get_reports(self):
        """Метод получения списка отчётов."""
        result = self.app.http_method.get(link=self.link)
        return self.app.http_method.return_result(response=result)

    def get_reports_id(self, reports_id: str):
        r"""Получение отчёта по его id.
        :param reports_id: Идентификатор отчёта.
        """
        result = self.app.http_method.get(link=f"{self.link}{reports_id}")
        return self.app.http_method.return_result(response=result)
