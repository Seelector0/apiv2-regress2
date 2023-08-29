import datetime


class ApiParcel:

    def __init__(self, app):
        self.app = app
        self.link = "parcels"

    def post_parcel(self, value, data: datetime = datetime.date.today()):
        r"""Метод создания партии.
        :param value: Идентификатор заказа.
        :param data: Дата отправки партии.
        """
        if type(value) is list:
            create_parcel = self.app.dict.form_parcel_body(orders_ids=value, data=str(data))
        else:
            create_parcel = self.app.dict.form_parcel_body(orders_ids=[value], data=str(data))
        result = self.app.http_method.post(link=self.link, json=create_parcel)
        return self.app.http_method.return_result(response=result)

    def get_parcels(self):
        """Метод получения списка партий."""
        result = self.app.http_method.get(link=self.link)
        return self.app.http_method.return_result(response=result)

    def get_parcel_id(self, parcel_id: str):
        r"""Получение партии по её id.
        :param parcel_id: Идентификатор партии.
        """
        result = self.app.http_method.get(link=f"{self.link}/{parcel_id}")
        return self.app.http_method.return_result(response=result)

    def patch_parcel(self, op: str, parcel_id: str, order_id: str):
        r"""Метод редактирования партии.
        :param op: Операция op, 'add' - добавление заказов, 'remove' - удаление заказов.
        :param order_id: Идентификатор партии.
        :param parcel_id: Идентификатор партии.
        """
        patch_parcel = self.app.dict.form_patch_body(op=op, path="orderIds", value=[order_id])
        result = self.app.http_method.patch(link=f"{self.link}/{parcel_id}", json=patch_parcel)
        return self.app.http_method.return_result(response=result)

    def patch_parcel_shipment_date(self, parcel_id: str, day: int):
        r"""Метод изменения даты доставки партии только для СД RussianPost.
        :param parcel_id: Идентификатор партии.
        :param day: Количество дней.
        """
        data = datetime.date.today()
        data += datetime.timedelta(days=day)
        patch_parcel = self.app.dict.form_patch_body(op="replace", path="shipmentDate", value=str(data))
        result = self.app.http_method.patch(link=f"{self.link}/{parcel_id}", json=patch_parcel)
        return self.app.http_method.return_result(response=result)

    def get_orders_in_parcel(self, parcel_id):
        """Получение списка заказов в партии."""
        order_in_parcel = []
        parcel_list = self.get_parcel_id(parcel_id=parcel_id)
        for order in parcel_list.json()["data"]["request"]["orderIds"]:
            order_in_parcel.append(order)
        return order_in_parcel
