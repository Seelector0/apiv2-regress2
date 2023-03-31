from random import randrange


class ApiOffers:

    def __init__(self, app):
        self.app = app

    def get_offers(self, types: str, delivery_service_code: str = None, payment_type: str = None,
                   delivery_point_number: str = None, format_: str = None):
        """Метод для получения списка офферов"""
        shop_id = self.app.shop.getting_list_shop_ids()
        warehouse_id = self.app.warehouse.getting_list_warehouse_ids()
        link_offers = "/offers"
        if format_ == "widget":
            body_offers = {
                "warehouseId": warehouse_id[0],
                "shopId": shop_id[0],
                "address": "г Москва, пр-кт Мира, д 45 стр 2",
                "declaredValue": randrange(1000, 5000),
                "height": randrange(10, 45),
                "length": randrange(10, 45),
                "width": randrange(10, 45),
                "weight": randrange(1, 10),
                "types[0]": types,
                "format": "widget"
            }
        else:
            body_offers = {
                "warehouseId": warehouse_id[0],
                "shopId": shop_id[0],
                "address":  "г Москва, пр-кт Мира, д 45 стр 2",
                "declaredValue": randrange(1000, 5000),
                "height": randrange(10, 45),
                "length": randrange(10, 45),
                "width": randrange(10, 45),
                "weight": randrange(1, 10),
                "paymentType": payment_type,
                "types[0]": types,
                "deliveryServiceCode": delivery_service_code,
                "deliveryPointNumber": delivery_point_number
            }
        return self.app.http_method.get(link=link_offers, params=body_offers)
