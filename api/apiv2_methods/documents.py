

class ApiDocument:

    def __init__(self, app):
        self.app = app

    def link_documents(self, parcel_id):
        """Метод получения ссылки для документов."""
        return f"{self.app.parcel.link}/{parcel_id}"

    def get_label(self, order_id: str, type_: str = None, size_format: str = None):
        r"""Метод получения этикетки.
        :param order_id: Идентификатор заказа.
        :param type_: Тип этикетки 'original' - этикетка от службы доставки, 'termo' - Этикетка по стандарту MetaShip.
        :param size_format: Размер этикетки для этикеток с типом original. Формат этикеток A4, A5, A6.
        """
        link = f"{self.app.order.link}/{order_id}/label"
        if type_:
            params = dict(type=type_)
        elif size_format:
            params = dict(size=size_format)
        else:
            return self.app.http_method.get(link=link)
        return self.app.http_method.get(link=link, params=params)

    def post_labels(self, parcel_id, order_ids: list):
        r"""Метод получения этикеток из партии.
        :param order_ids: Список идентификаторов заказа.
        :param parcel_id: Id партии.
        """
        labels = dict(orderIds=order_ids)
        return self.app.http_method.post(link=f"{self.link_documents(parcel_id=parcel_id)}/labels", json=labels)

    def get_acceptance(self, parcel_id):
        """Метод получения АПП."""
        return self.app.http_method.get(link=f"{self.link_documents(parcel_id=parcel_id)}/acceptance")

    def get_files(self, parcel_id):
        """Получение документов."""
        return self.app.http_method.get(link=f"{self.link_documents(parcel_id=parcel_id)}/files")
