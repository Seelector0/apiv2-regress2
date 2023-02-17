from random import randrange


class ApiOffers:

    def __init__(self, app):
        self.app = app

    def get_offers(self, warehouse_id, shop_id, types, headers, delivery_service_code=None, payment_type=None,
                   format_=None):
        """Метод для получения списка офферов"""
        if format_ is None:
            body_offers = {
                "address":  "г Москва, пр-кт Мира, д 45 стр 2",
                "declaredValue": randrange(1000, 5000),
                "height": randrange(10, 45),
                "length": randrange(10, 45),
                "width": randrange(10, 45),
                "weight": randrange(1, 10),
                "warehouseId": warehouse_id,
                "shopId": shop_id,
                "paymentType": payment_type,
                "types[0]": types,
                "deliveryServiceCode": delivery_service_code,
            }
            result_offers = self.app.http_method.get(link="/offers", params=body_offers, headers=headers)
            return result_offers
        elif format_ == "widget":
            body_offers = {
                "address": "г Москва, пр-кт Мира, д 45 стр 2",
                "declaredValue": randrange(1000, 5000),
                "height": randrange(10, 45),
                "length": randrange(10, 45),
                "width": randrange(10, 45),
                "weight": randrange(1, 10),
                "warehouseId": warehouse_id,
                "shopId": shop_id,
                "types[0]": types,
                "format": "widget"
            }
            result_offers = self.app.http_method.get(link="/offers", params=body_offers, headers=headers)
            return result_offers
