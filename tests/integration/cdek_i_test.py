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


@allure.description("Подключение настроек службы доставки СД Cdek")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.cdek())


@allure.description("Создание заказа по CД Cdek")
def test_create_single_order(app, shop_id, warehouse_id, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type="Paid", delivery_type="Courier", service="Cdek",
                                          tariff=choice(INFO.cdek_courier_tariffs),
                                          shared_data=shared_data["cdek_i"]["order_ids_single"])


@allure.description("Создание партии СД Cdek")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data, shared_delivery_service="cdek_i",
                                       types="order_ids_single")


@allure.description("Получение этикеток СД Cdek")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_label(app, labels, shared_data):
    CommonParcels.test_get_label_common(app=app, labels=labels,
                                        shared_data=shared_data["cdek_i"]["order_ids_in_parcel"])


@allure.description("Получения оригинальных этикеток CД Cdek в формате A4, A5, A6")
@pytest.mark.parametrize("format_", ["A4", "A5", "A6"])
def test_get_original_labels(app, format_, shared_data):
    CommonParcels.test_get_label_common(app=app, format_=format_,
                                        shared_data=shared_data["cdek_i"]["order_ids_in_parcel"])
