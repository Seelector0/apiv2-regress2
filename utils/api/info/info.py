import datetime


class ApiInfo:

    def __init__(self, app):
        self.app = app

    def delivery_time_schedules(self, delivery_service_code: str, day: str = None):
        """Получение интервалов доставки конкретной СД"""
        if day == "today":
            params = {
                "deliveryServiceCode": delivery_service_code,
                "deliveryDate": f"{datetime.date.today()}",
                "shopId": self.app.shop.getting_list_shop_ids()[0],
                "postalCode": "101000"
            }
        else:
            params = {
                "deliveryServiceCode": delivery_service_code,
            }
        return self.app.http_method.get(link="info/delivery_time_schedules", params=params)

    def delivery_service_points(self, delivery_service_code: str, city_raw="г. Москва"):
        """Получение списка ПВЗ конкретной СД"""
        params = {
            "deliveryServiceCode": delivery_service_code,
            "shopId": self.app.shop.getting_list_shop_ids()[0],
            "cityRaw": city_raw
        }
        return self.app.http_method.get(link="customer/info/delivery_service_points", params=params)

    def info_vats(self, delivery_service_code: str):
        """Получение списка ставок НДС, которые умеет принимать и обрабатывать конкретная СД"""
        params = {
            "deliveryServiceCode": delivery_service_code
        }
        return self.app.http_method.get(link="info/vats", params=params)

    def intake_offices(self, delivery_service_code: str):
        """Получение списка точек сдачи"""
        params = {
            "deliveryServiceCode": delivery_service_code
        }
        return self.app.http_method.get(link="info/intake_offices", params=params)

    def info_statuses(self):
        """Получение полного актуального списка возможных статусов заказа"""
        result_info_statuses = self.app.http_method.get(link="/info/statuses")
        return result_info_statuses

    def info_delivery_service_services(self, code: str):
        """Получение информации о дополнительных услугах поддерживаемых СД"""
        return self.app.http_method.get(link=f"info/delivery_service/{code}/services")

    def user_clients(self):
        """Получение списка ключей"""
        return self.app.http_method.get(link="user/clients")

    def user_clients_id(self, user_id: str):
        """Получение информации о ключе подключения по id"""
        return self.app.http_method.get(link=f"user/clients/{user_id}")

    def info_address(self, raw: str = "101000, г Москва"):
        """Разбор адреса"""
        params = {
            "raw": raw
        }
        return self.app.http_method.get(link="info/address", parsms=params)
