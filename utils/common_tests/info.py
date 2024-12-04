from random import choice
from utils.checking import Checking
from utils.utils import check_shared_data


class CommonInfo:

    def __init__(self, app):
        self.app = app

    def test_delivery_service_points_common(self, shop_id, delivery_service_code):
        """Получение списка ПВЗ"""
        delivery_service_points = self.app.info.get_delivery_service_points(shop_id=shop_id,
                                                                            delivery_service_code=delivery_service_code)
        Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
        Checking.check_response_is_not_empty(response=delivery_service_points)
        Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                             expected_value=delivery_service_code)

    def test_delivery_time_schedules_common(self, shop_id, delivery_service_code, data=None, tariff_id=None,
                                            order_id=None, shared_data=None):
        """Получения сроков доставки"""
        if shared_data:
            check_shared_data(shared_data)
            order_id = choice(shared_data)
        delivery_time_schedules = self.app.info.get_delivery_time_schedules(shop_id=shop_id, data=data,
                                                                            tariff_id=tariff_id,
                                                                            delivery_service_code=delivery_service_code,
                                                                            order_id=order_id)
        Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
        Checking.checking_json_key(response=delivery_time_schedules, expected_value=["schedule", "intervals"])
        Checking.check_keys_present_in_list_items(response=delivery_time_schedules, list_key="intervals",
                                                  key_names=["date", "from", "to"])
        if delivery_service_code == "Dalli":
            Checking.check_keys_present_in_list_items(response=delivery_time_schedules, list_key="intervals",
                                                      key_names=["zone"])
