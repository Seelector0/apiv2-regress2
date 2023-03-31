import json


class ApiDocument:

    def __init__(self, app):
        self.app = app

    def link_parcels(self):
        parcels_ids = self.app.parcel.getting_list_of_parcels_ids()
        for parcel_id in parcels_ids:
            return f"/parcels/{parcel_id}"

    def get_label(self, order_id: str, type_: str = "original"):
        """Метод получения этикетки"""
        link = f"/orders/{order_id}/label"
        if type_ == "termo":
            params = {
                "type": "termo"
            }
            return self.app.http_method.get(link=link, params=params)
        else:
            return self.app.http_method.get(link=link)

    def get_labels_from_parcel(self, order_ids: list):
        """Метод получения этикеток из партии"""
        json_labels_from_parcel = json.dumps(
            {
                "orderIds": order_ids
            }
        )
        return self.app.http_method.post(link=f"{self.link_parcels()}/labels", data=json_labels_from_parcel)

    def get_app(self):
        """Метод получения АПП"""
        return self.app.http_method.get(link=f"{self.link_parcels()}/acceptance")

    def get_documents(self):
        """Получение документов"""
        return self.app.http_method.get(link=f"{self.link_parcels()}/files")
