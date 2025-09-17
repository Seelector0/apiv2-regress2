from random import choice
from utils.checking import Checking
from utils.response_schemas import SCHEMAS
from utils.utils import check_shared_data


class CommonInfo:

    def __init__(self, app):
        self.app = app

    def test_delivery_service_points_common(self, shop_id, delivery_service_code):
        """Получение списка ПВЗ"""
        delivery_service_points = self.app.info.get_delivery_service_points(shop_id=shop_id,
                                                                            delivery_service_code=delivery_service_code)
        Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
        Checking.check_json_schema(response=delivery_service_points, schema=SCHEMAS.info.info_delivery_service_point)
        Checking.check_response_is_not_empty(response=delivery_service_points)
        Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                             expected_value=delivery_service_code)

    def test_delivery_time_schedules_common(self, shop_id, delivery_service_code, data=None, tariff_id=None,
                                            order_id=None, shared_data=None, intake_date=None, warehouse_id=None,
                                            fias_id=None):
        """Получения сроков доставки"""
        if shared_data:
            check_shared_data(shared_data)
            order_id = choice(shared_data)
        delivery_time_schedules = self.app.info.get_delivery_time_schedules(shop_id=shop_id, data=data,
                                                                            tariff_id=tariff_id,
                                                                            delivery_service_code=delivery_service_code,
                                                                            order_id=order_id, intake_date=intake_date,
                                                                            warehouse_id=warehouse_id, fias_id=fias_id)
        Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
        Checking.check_json_schema(response=delivery_time_schedules, schema=SCHEMAS.info.info_schedule)


