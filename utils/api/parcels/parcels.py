import datetime
import json


class ApiParcel:

    def __init__(self, app):
        self.app = app

    def create_parcel(self, order_id: list, headers: dict):
        """Метод создания партии"""
        json_create_parcel = json.dumps(
            {
                "orderIds": [order_id],
                "shipmentDate": f"{datetime.date.today()}"
            }
        )
        result_post_parcel = self.app.http_method.post(link="/parcels", data=json_create_parcel, headers=headers)
        return result_post_parcel

    def get_parcels(self, headers: dict):
        """Метод получения списка партий"""
        result_get_parcels = self.app.http_method.get(link="/parcels", headers=headers)
        return result_get_parcels

    def get_parcel_by_id(self, parcel_id: str, headers: dict):
        """Получение партии по её id"""
        result_get_parcel_by_id = self.app.http_method.get(link=f"/parcels/{parcel_id}", headers=headers)
        return result_get_parcel_by_id

    def change_parcel_orders(self, op: str, order_id, parcel_id: str, headers: dict):
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
            result_add_parcel_order = self.app.http_method.patch(link=f"/parcels/{parcel_id}",
                                                                 data=json_add_parcel_order,
                                                                 headers=headers)
            return result_add_parcel_order
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
            result_add_parcel_order = self.app.http_method.patch(link=f"/parcels/{parcel_id}",
                                                                 data=json_remove_parcel_order,
                                                                 headers=headers)
            return result_add_parcel_order

    def change_parcel_shipment_date(self, parcel_id: str, headers: dict, day):
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
        result_change_parcel_shipment_date = self.app.http_method.patch(link=f"/parcels/{parcel_id}",
                                                                        data=json_change_parcel_shipment_date,
                                                                        headers=headers)
        return result_change_parcel_shipment_date

    def get_order_in_parcel(self, parcel_id, headers):
        """Получение списка заказов в партии"""
        order_in_parcel = []
        parcel_list = self.get_parcel_by_id(parcel_id=parcel_id, headers=headers)
        for order in parcel_list.json()["data"]["request"]["orderIds"]:
            order_in_parcel.append(order)
        return order_in_parcel

    def get_parcel_id(self, headers):
        """Получение списка id партий"""
        list_parcel_id = []
        parcel_list = self.get_parcels(headers=headers)
        for parcel_id in parcel_list.json():
            list_parcel_id.append(parcel_id["id"])
        return list_parcel_id
