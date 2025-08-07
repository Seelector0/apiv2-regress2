from utils.common_tests import CommonConnections, CommonOrders, CommonParcels
import pytest
import allure


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_without_pickup(app, connections, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(pickup=False, warehouse_type="warehouse_without_pickup",
                                              shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД Pecom")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.pecom())


@allure.description("Создание заказа по CД Pecom")
def test_create_single_order(app, shop_id, warehouse_without_pickup, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id,
                                          warehouse_id=warehouse_without_pickup,
                                          payment_type="Paid", delivery_type="Courier", service="Pecom",
                                          tariff="3", shared_data=shared_data["pecom_i"]["order_ids"])


@allure.description("Создание партии СД Pecom")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_delivery_service="pecom_i", shared_data=shared_data)


@allure.description("Получение этикеток СД Pecom")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, labels="termo",
                                        shared_data=shared_data["pecom_i"]["order_ids_in_parcel"])
