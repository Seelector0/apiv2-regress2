

class ApiInfo:

    def __init__(self, app):
        self.app = app

    def delivery_time_schedules(self, delivery_service_code: str):
        """Получение интервалов доставки конкретной СД"""
        params = {
            "deliveryServiceCode": delivery_service_code,
        }
        result_delivery_time_schedules = self.app.http_method.get(link="/info/delivery_time_schedules", params=params)
        return result_delivery_time_schedules

    def delivery_service_points(self, delivery_service_code: str, city_raw="г. Москва"):
        shop_id = self.app.shop.get_shops_id()
        """Получение списка ПВЗ конкретной СД"""
        params = {
            "deliveryServiceCode": delivery_service_code,
            "shopId": shop_id[0],
            "cityRaw": city_raw
        }
        result_delivery_service_points = self.app.http_method.get(link="/customer/info/delivery_service_points",
                                                                  params=params)
        return result_delivery_service_points

    def info_vats(self, delivery_service_code: str):
        """Получение списка ставок НДС, которые умеет принимать и обрабатывать конкретная СД"""
        params = {
            "deliveryServiceCode": delivery_service_code
        }
        result_info_vats = self.app.http_method.get(link="/info/vats", params=params)
        return result_info_vats

    def intake_offices(self, delivery_service_code: str):
        """Получение списка точек сдачи"""
        params = {
            "deliveryServiceCode": delivery_service_code
        }
        result_intake_offices = self.app.http_method.get(link="/info/intake_offices", params=params)
        return result_intake_offices

    def info_statuses(self):
        """Получение полного актуального списка возможных статусов заказа"""
        result_info_statuses = self.app.http_method.get(link="/info/statuses")
        return result_info_statuses

    def info_delivery_service_services(self, code: str):
        """Получение информации о дополнительных услугах поддерживаемых СД"""
        result_info_delivery_service_services = self.app.http_method.get(link=f"/info/delivery_service/{code}/services")
        return result_info_delivery_service_services

    def user_clients(self):
        """Получение списка ключей"""
        result_user_clients = self.app.http_method.get(link="/user/clients")
        return result_user_clients

    def user_clients_id(self, user_id: str):
        """Получение информации о ключе подключения по id"""
        result_user_clients_id = self.app.http_method.get(link=f"/user/clients/{user_id}")
        return result_user_clients_id

    def info_address(self, raw: str = "101000, г Москва"):
        """Разбор адреса"""
        params = {
            "raw": raw
        }
        result_info_address = self.app.http_method.get(link="/info/address", parsms=params)
        return result_info_address
