from utils.http_methods import HttpMethods
import datetime
import time
import json


class ApiParcel:

    @staticmethod
    def create_parcel(order_ids: list, headers: dict, sec: float = 2):
        time.sleep(sec)
        """Метод создания партии"""
        json_create_parcel = json.dumps(
            {
                "orderIds": order_ids,
                "shipmentDate": f"{datetime.date.today()}"
            }
        )
        result_post_parcel = HttpMethods.post(link="/parcels", data=json_create_parcel, headers=headers)
        return result_post_parcel

    @staticmethod
    def get_parcels(headers: dict):
        """Метод получения списка партий"""
        result_get_parcels = HttpMethods.get(link="/parcels", headers=headers)
        return result_get_parcels

    @staticmethod
    def get_parcel_by_id(parcel_id: str, headers: dict):
        """Получение партии по её id"""
        result_get_parcel_by_id = HttpMethods.get(link=f"/parcels/{parcel_id}", headers=headers)
        return result_get_parcel_by_id

    @staticmethod
    def change_parcel_orders(order_id: list, parcel_id: str, op: str, headers: dict):
        """Метод редактирования партии - добавление(add), удаление(remove) заказов"""
        orders = []
        if op == "add":
            json_add_parcel_order = json.dumps(
                [
                    {
                        "op": "add",
                        "path": "orderIds",
                        "value": orders.append(order_id)
                    }
                ]
            )
            result_add_parcel_order = HttpMethods.patch(link=f"/parcels/{parcel_id}", data=json_add_parcel_order,
                                                           headers=headers)
            return result_add_parcel_order
        elif op == "remove":
            json_remove_parcel_order = json.dumps(
                [
                    {
                        "op": "remove",
                        "path": "orderIds",
                        "value": orders.remove(order_id)
                    }
                ]
            )
            result_add_parcel_order = HttpMethods.patch(link=f"/parcels/{parcel_id}", data=json_remove_parcel_order,
                                                        headers=headers)
            return result_add_parcel_order

    @staticmethod
    def change_parcel_shipment_date(parcel_id: str, data: str, headers: dict):
        """Метод изменения даты доставки партии"""
        json_change_parcel_shipment_date = json.dumps(
            [
                {
                    "op": "replace",
                    "path": "shipmentDate",
                    "value": f"{data}"
                }
            ]
        )
        result_change_parcel_shipment_date = HttpMethods.patch(link=f"/parcels/{parcel_id}",
                                                               data=json_change_parcel_shipment_date, headers=headers)
        return result_change_parcel_shipment_date

    @staticmethod
    def get_labels_from_parcel(parcel_id: str, order_id: str, headers:dict):
        """Метод получения этикеток из партии"""
        orders = []
        json_get_labels_from_parcel = json.dumps(
            {
                "orderIds": orders.append(order_id)
            }
        )
        result_get_labels_from_parcel = HttpMethods.post(link=f"/parcels/{parcel_id}/labels",
                                                         data=json_get_labels_from_parcel, headers=headers)
        return result_get_labels_from_parcel

    @staticmethod
    def get_app(parcel_id, headers):
        """Метод получения АПП"""
        result_get_app = HttpMethods.get(link=f"/v2/parcels/{parcel_id}/acceptance", headers=headers)
        return result_get_app

    @staticmethod
    def get_files(parcel_id, headers):
        result_get_files = HttpMethods.get(link=f"/v2/parcels/{parcel_id}/files", headers=headers)
        return result_get_files
