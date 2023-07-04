import datetime
import allure
import json


class ApiParcel:

    def __init__(self, app):
        self.app = app
        self.link = "parcels"

    def post_parcel(self, order_id: str, all_orders: bool = False, data: str = None):
        r"""Метод создания партии.
        :param order_id: Идентификатор заказа.
        :param all_orders: Флаг True отправляет списком заказы в партию.
        :param data: Дата отправки партии.
        """
        if data is None:
            data = datetime.date.today()
        if all_orders:
            create_parcel = {
                "orderIds": [*order_id],
                "shipmentDate": f"{data}"
            }
        else:
            create_parcel = {
                "orderIds": [order_id],
                "shipmentDate": f"{data}"
            }
        with allure.step(title=f"Requests: {create_parcel}"):
            result = self.app.http_method.post(link=self.link, data=json.dumps(create_parcel))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def get_parcels(self):
        """Метод получения списка партий."""
        result = self.app.http_method.get(link=self.link)
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def get_parcel_id(self, parcel_id: str):
        r"""Получение партии по её id.
        :param parcel_id: Идентификатор партии.
        """
        result = self.app.http_method.get(link=f"{self.link}/{parcel_id}")
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def patch_parcel(self, op: str, parcel_id: str, order_id: str):
        r"""Метод редактирования партии.
        :param op: Операция op, 'add' - добавление заказов, 'remove' - удаление заказов.
        :param order_id: Идентификатор партии.
        :param parcel_id: Идентификатор партии.
        """
        if op:
            patch_parcel = [
                {
                    "op": op,
                    "path": "orderIds",
                    "value": [order_id]
                }
            ]
        else:
            raise ValueError(f"Выбрана не верная операция {op}, выберите add или remove")
        with allure.step(title=f"Requests: {patch_parcel}"):
            result = self.app.http_method.patch(link=f"{self.link}/{parcel_id}", data=json.dumps(patch_parcel))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def patch_parcel_shipment_date(self, parcel_id: str, day: int):
        r"""Метод изменения даты доставки партии только для СД RussianPost.
        :param parcel_id: Идентификатор партии.
        :param day: Количество дней.
        """
        data: datetime.date = datetime.date.today()
        data += datetime.timedelta(days=day)
        patch_parcel = [
            {
                "op": "replace",
                "path": "shipmentDate",
                "value": f"{data}"
            }
        ]
        with allure.step(title=f"Requests: {patch_parcel}"):
            result = self.app.http_method.patch(link=f"{self.link}/{parcel_id}", data=json.dumps(patch_parcel))
        with allure.step(title=f"Response: {result.json()}"):
            return result

    def get_orders_in_parcel(self, parcel_id):
        """Получение списка заказов в партии."""
        order_in_parcel = []
        parcel_list = self.get_parcel_id(parcel_id=parcel_id)
        for order in parcel_list.json()["data"]["request"]["orderIds"]:
            order_in_parcel.append(order)
        return order_in_parcel

    def getting_list_of_parcels_ids(self):
        """Получение списка id партий."""
        list_parcel_id = []
        parcel_list = self.get_parcels()
        for parcel_id in parcel_list.json():
            list_parcel_id.append(parcel_id["id"])
        return list_parcel_id
