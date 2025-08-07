import pytest
import allure
from random import randrange
from utils.common_tests import CommonConnections, CommonOrders, CommonParcels


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_id(app, connections, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД YandexDelivery")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.yandex_delivery())


@allure.description("Создание Courier заказа по CД YandexDelivery")
def test_create_single_order(app, shop_id, warehouse_id, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          shop_barcode=f"{randrange(100000000, 999999999)}",
                                          payment_type="Paid", delivery_type="Courier",
                                          service="YandexDelivery", delivery_sum=0,
                                          shared_data=shared_data["yandex_delivery_i"]["order_ids"])


@allure.description("Создание партии CД YandexDelivery")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_delivery_service="yandex_delivery_i", shared_data=shared_data)


@allure.description("Получение этикеток СД YandexDelivery")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels(app, labels, shared_data):
    CommonParcels.test_get_label_common(app=app, labels=labels,
                                        shared_data=shared_data["yandex_delivery_i"]["order_ids_in_parcel"])
