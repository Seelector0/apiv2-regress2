

class ApiInfo:

    def __init__(self, app):
        self.app = app

    def delivery_service_points(self, delivery_service_code, headers):
        """Получение списка ПВЗ конкретной СД"""
        data = {
            "deliveryServiceCode": delivery_service_code,
            "cityRaw": "г. Москва"
        }
        result_delivery_service_points = self.app.http_method.get(link="/customer/info/delivery_service_points",
                                                                  params=data, headers=headers)
        return result_delivery_service_points

    def info_vats(self, delivery_service_code, headers):
        """Получение списка ставок НДС, которые умеет принимать и обрабатывать конкретная СД"""
        data = {
            "deliveryServiceCode": delivery_service_code
        }
        result_info_vats = self.app.http_method.get(link="/info/vats", params=data, headers=headers)
        return result_info_vats
