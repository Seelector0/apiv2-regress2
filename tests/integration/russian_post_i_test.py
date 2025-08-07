import pytest
import allure
from random import choice
from utils.global_enums import INFO
from utils.common_tests import CommonConnections, CommonOrders, CommonParcels


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_id(app, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД RussianPost")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.russian_post())


@allure.description("Создание Courier заказа по СД RussianPost")
def test_create_order_courier(app, shop_id, warehouse_id, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type="Paid", delivery_type="Courier", service="RussianPost",
                                          tariff=choice(INFO.rp_courier_tariffs),
                                          shared_data_order_type=shared_data["russian_post_i"]["orders_courier"])


@allure.description("Создание партии СД RussianPost")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data, shared_delivery_service="russian_post_i",
                                       types="orders_courier")


@allure.description("Получение этикетки СД RussianPost")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data["russian_post_i"]["order_ids_in_parcel"])
