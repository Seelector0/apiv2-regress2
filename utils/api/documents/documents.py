import json


class ApiDocument:

    def __init__(self, app):
        self.app = app

    def get_label(self, order_id: str, headers: dict):
        """Метод получения этикетки заказа"""
        result_get_label = self.app.http_method.get(link=f"/orders/{order_id}/label", headers=headers)
        return result_get_label

    def get_labels_from_parcel(self, parcel_id: str, order_ids: list, headers:dict):
        """Метод получения этикеток из партии"""
        json_get_labels_from_parcel = json.dumps(
            {
                "orderIds": [order_ids]
            }
        )
        result_get_labels_from_parcel = self.app.http_method.post(link=f"/parcels/{parcel_id}/labels",
                                                                  data=json_get_labels_from_parcel, headers=headers)
        return result_get_labels_from_parcel

    def get_app(self, parcel_id, headers):
        """Метод получения АПП"""
        result_get_app = self.app.http_method.get(link=f"/parcels/{parcel_id}/acceptance", headers=headers)
        return result_get_app

    def get_documents(self, parcel_id, headers):
        """Получение документов"""
        result_get_files = self.app.http_method.get(link=f"/parcels/{parcel_id}/files", headers=headers)
        return result_get_files
