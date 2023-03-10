import datetime
import json


class ApiParcel:

    def __init__(self, app):
        self.app = app
        self.link = "/parcels"

    def create_parcel(self, order_id: str, all_orders: bool = False):
        """Метод создания партии"""
        if all_orders:
            json_create_parcel = json.dumps(
                {
                    "orderIds": [*order_id],
                    "shipmentDate": f"{datetime.date.today()}"
                }
            )
            result_post_parcel = self.app.http_method.post(link=self.link, data=json_create_parcel)
        else:
            json_create_parcel = json.dumps(
                {
                    "orderIds": [order_id],
                    "shipmentDate": f"{datetime.date.today()}"
                }
            )
            result_post_parcel = self.app.http_method.post(link=self.link, data=json_create_parcel)
        return result_post_parcel

    def get_parcels(self):
        """Метод получения списка партий"""
        result_get_parcels = self.app.http_method.get(link=self.link)
        return result_get_parcels

    def get_parcel_by_id(self, parcel_id: str):
        """Получение партии по её id"""
        result_get_parcel_by_id = self.app.http_method.get(link=f"{self.link}/{parcel_id}")
        return result_get_parcel_by_id

    def change_parcel_orders(self, op: str, order_id, parcel_id: str):
        """Метод редактирования партии - добавление(add), удаление(remove) заказов"""
        if op == "add":
            json_add_parcel_order = json.dumps(
                [
                    {
                        "op": "add",
                        "path": "orderIds",
                        "value": [order_id]
                    }
                ]
            )
            result_add_parcel = self.app.http_method.patch(link=f"{self.link}/{parcel_id}", data=json_add_parcel_order)
            return result_add_parcel
        elif op == "remove":
            json_remove_parcel_order = json.dumps(
                [
                    {
                        "op": "remove",
                        "path": "orderIds",
                        "value": [order_id]
                    }
                ]
            )
            result_remove_parcel = self.app.http_method.patch(link=f"{self.link}/{parcel_id}",
                                                              data=json_remove_parcel_order)
            return result_remove_parcel

    def change_parcel_shipment_date(self, parcel_id: str, day):
        """Метод изменения даты доставки партии"""
        data: datetime.date = datetime.date.today()
        data += datetime.timedelta(days=day)
        json_change_parcel_shipment_date = json.dumps(
            [
                {
                    "op": "replace",
                    "path": "shipmentDate",
                    "value": f"{data}"
                }
            ]
        )
        result_change_parcel_shipment_date = self.app.http_method.patch(link=f"{self.link}/{parcel_id}",
                                                                        data=json_change_parcel_shipment_date)
        return result_change_parcel_shipment_date

    def get_order_in_parcel(self, parcel_id):
        """Получение списка заказов в партии"""
        order_in_parcel = []
        parcel_list = self.get_parcel_by_id(parcel_id=parcel_id)
        for order in parcel_list.json()["data"]["request"]["orderIds"]:
            order_in_parcel.append(order)
        return order_in_parcel

    def get_parcels_id(self):
        """Получение списка id партий"""
        list_parcel_id = []
        parcel_list = self.get_parcels()
        for parcel_id in parcel_list.json():
            list_parcel_id.append(parcel_id["id"])
        return list_parcel_id
