import pytest
import allure
from utils.common_tests import CommonConnections, CommonOrders, CommonParcels


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_id(app, connections, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД FivePost")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.five_post())


@allure.description("Создание DeliveryPoint заказа по СД FivePost")
def test_create_single_order(app, shop_id, warehouse_id, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type="Paid", delivery_type="DeliveryPoint", service="FivePost",
                                          delivery_point_code="006bf88a-5186-45d9-9911-89d37f1edc86",
                                          shared_data=shared_data["five_post_i"]["order_ids_single"])


@allure.description("Создание партии СД FivePost")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data, shared_delivery_service="five_post_i",
                                       types="order_ids_single")


@allure.description("Получение этикеток СД FivePost")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data["five_post_i"]["order_ids_in_parcel"])
