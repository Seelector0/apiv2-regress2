import pytest
import allure
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels
from utils.dates import tomorrow


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_id(app, connections, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД MagnitPost")
def test_aggregation_delivery_services(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          delivery_service="MagnitPost",
                                                          connection_settings=app.settings.magnit_post(),
                                                          moderation_settings=admin.moderation.magnit_post)


@allure.description("Создание многоместного заказа по CД MagnitPost")
def test_create_multi_order(app, shop_id, warehouse_id, connections, shared_data):
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                         payment_type="Paid", delivery_type="DeliveryPoint", service="MagnitPost",
                                         delivery_point_code="63122",
                                         shared_data=shared_data["magnitpost_a"]["order_ids"])


@allure.description("Создание заказа по CД MagnitPost")
def test_create_single_order(app, shop_id, warehouse_id, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type="Paid", delivery_type="DeliveryPoint", service="MagnitPost",
                                          delivery_point_code="63122",
                                          shared_data=shared_data["magnitpost_a"]["order_ids"])


@allure.description("Получение списка заказов CД MagnitPost")
def test_get_orders(app, shared_data):
    CommonOrders.test_get_orders_common(app=app, shared_delivery_service="magnitpost_a", shared_data=shared_data)


@allure.description("Получение информации о заказе CД MagnitPost")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["magnitpost_a"]["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа CД MagnitPost")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["magnitpost_a"]["order_ids"])


@allure.description("Получение подробной информации о заказе CД MagnitPost")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["magnitpost_a"]["order_ids"])

@allure.description("Получение кода выдачи заказа для СД FivePost")
def test_generate_security_code(app, shared_data):
    CommonOrders.test_generate_security_common(app=app, shared_data=shared_data["magnitpost_a"]["order_ids"])
