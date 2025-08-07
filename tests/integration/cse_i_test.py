import pytest
import allure
from utils.dates import today
from utils.common_tests import CommonConnections, CommonOrders, CommonParcels


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_without_pickup(app, connections, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(pickup=False, warehouse_type="warehouse_without_pickup",
                                              shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД Cse")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.cse())


@allure.description("Создание заказа по СД Cse")
def test_create_single_order(app, shop_id, warehouse_without_pickup, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id,
                                          warehouse_id=warehouse_without_pickup, payment_type="Paid",
                                          delivery_type="Courier", service="Cse", tariff="64", date_pickup=str(today),
                                          shared_data=shared_data["cse_i"]["order_ids"])


@allure.description("Создание партии СД Cse")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_delivery_service="cse_i", shared_data=shared_data)


@allure.description("Получение этикеток СД Cse")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels(app, labels, shared_data):
    CommonParcels.test_get_label_common(app=app, labels=labels,
                                        shared_data=shared_data["cse_i"]["order_ids_in_parcel"])
