from utils.checking import Checking
from utils.global_enums import INFO


class CommonInfo:

    @staticmethod
    def test_delivery_service_points_common(app, shop_id, delivery_service_code):
        """Получение списка ПВЗ"""
        delivery_service_points = app.info.get_delivery_service_points(shop_id=shop_id,
                                                                       delivery_service_code=delivery_service_code)
        Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
        Checking.check_response_is_not_empty(response=delivery_service_points)
        Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                             expected_value=delivery_service_code)

    @staticmethod
    def test_delivery_time_schedules_common(app, shop_id, delivery_service_code, data=None, tariff_id=None):
        """Получения сроков доставки"""
        delivery_time_schedules = app.info.get_delivery_time_schedules(shop_id=shop_id, data=data, tariff_id=tariff_id,
                                                                       delivery_service_code=delivery_service_code)
        Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
        if tariff_id == "1":
            Checking.checking_json_value(response=delivery_time_schedules, key_name="intervals",
                                         expected_value=INFO.dalli_intervals_1)
        elif tariff_id == "2":
            Checking.checking_json_value(response=delivery_time_schedules, key_name="intervals",
                                         expected_value=INFO.dalli_intervals_2)
        elif tariff_id == "11":
            Checking.checking_json_value(response=delivery_time_schedules, key_name="intervals",
                                         expected_value=INFO.dalli_intervals_11)
