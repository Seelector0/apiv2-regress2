from fixture.database import DataBase
from environment import ENV_OBJECT


class ApiDocument:

    def __init__(self, app):
        self.app = app
        self.database = DataBase(database=ENV_OBJECT.db_connections())

    def link_documents(self):
        """Метод получения ссылки для документов."""
        return f"{self.app.parcel.link}/{self.database.metaship.get_list_parcels()[0]}"

    def get_label(self, order_id: str, type_: str = None, size_format: str = None):
        r"""Метод получения этикетки.
        :param order_id: Идентификатор заказа.
        :param type_: Тип этикетки 'original' - этикетка от службы доставки, 'termo' - Этикетка по стандарту MetaShip.
        :param size_format: Размер этикетки для этикеток с типом original. Формат этикеток A4, A5, A6.
        """
        link = f"{self.app.order.link}/{order_id}/label"
        if type_:
            params = {
                "type": type_
            }
        elif size_format:
            params = {
                "size": size_format
            }
        else:
            return self.app.http_method.get(link=link)
        return self.app.http_method.get(link=link, params=params)

    def post_labels(self, order_ids: list):
        r"""Метод получения этикеток из партии.
        :param order_ids: Список идентификаторов заказа.
        """
        labels = {
            "orderIds": order_ids
        }
        return self.app.http_method.post(link=f"{self.link_documents()}/labels", json=labels)

    def get_acceptance(self):
        """Метод получения АПП."""
        return self.app.http_method.get(link=f"{self.link_documents()}/acceptance")

    def get_files(self):
        """Получение документов."""
        return self.app.http_method.get(link=f"{self.link_documents()}/files")
