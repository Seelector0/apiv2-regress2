from random import randrange


class ApiOffers:

    def __init__(self, app):
        self.app = app

    def get_offers(self, types: str, delivery_service_code: str = None, payment_type: str = None, format_: str = None):
        """Метод для получения списка офферов"""
        shop_id = self.app.shop.get_shops_id()
        warehouse_id = self.app.warehouse.get_warehouses_id()
        if format_ == "widget":
            body_offers = {
                "address": "г Москва, пр-кт Мира, д 45 стр 2",
                "declaredValue": randrange(1000, 5000),
                "height": randrange(10, 45),
                "length": randrange(10, 45),
                "width": randrange(10, 45),
                "weight": randrange(1, 10),
                "warehouseId": warehouse_id[0],
                "shopId": shop_id[0],
                "types[0]": types,
                "format": "widget"
            }
            result_offers = self.app.http_method.get(link="/offers", params=body_offers)
            return result_offers
        else:
            body_offers = {
                "address":  "г Москва, пр-кт Мира, д 45 стр 2",
                "declaredValue": randrange(1000, 5000),
                "height": randrange(10, 45),
                "length": randrange(10, 45),
                "width": randrange(10, 45),
                "weight": randrange(1, 10),
                "warehouseId": warehouse_id[0],
                "shopId": shop_id[0],
                "paymentType": payment_type,
                "types[0]": types,
                "deliveryServiceCode": delivery_service_code,
            }
            result_offers = self.app.http_method.get(link="/offers", params=body_offers)
            return result_offers
