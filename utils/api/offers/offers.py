from random import randrange


class ApiOffers:

    def __init__(self, app):
        self.app = app

    def get_offers(self, warehouse_id, shop_id, payment_type, types, delivery_service_code, headers):
        body = {
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
        result_offers = self.app.http_method.get(link="/offers", params=body, headers=headers)
        return result_offers
