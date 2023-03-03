import json


class ApiDocument:

    def __init__(self, app):
        self.app = app

    def get_label(self, order_id: str, type_: str = None):
        """Метод получения этикетки"""
        if type_ == "termo":
            params = {
                "type": "termo"
            }
            result_get_label = self.app.http_method.get(link=f"/orders/{order_id}/label", params=params)
            return result_get_label
        else:
            result_get_label = self.app.http_method.get(link=f"/orders/{order_id}/label")
            return result_get_label

    def get_labels_from_parcel(self, parcel_id: str, order_ids: list):
        """Метод получения этикеток из партии"""
        json_labels_from_parcel = json.dumps(
            {
                "orderIds": order_ids
            }
        )
        result_get_labels_from_parcel = self.app.http_method.post(link=f"/parcels/{parcel_id}/labels",
                                                                  data=json_labels_from_parcel)
        return result_get_labels_from_parcel

    def get_app(self, parcel_id: str):
        """Метод получения АПП"""
        result_get_app = self.app.http_method.get(link=f"/parcels/{parcel_id}/acceptance")
        return result_get_app

    def get_documents(self, parcel_id: str):
        """Получение документов"""
        result_get_files = self.app.http_method.get(link=f"/parcels/{parcel_id}/files")
        return result_get_files
