import pytest
import allure
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_id(app, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД PsbLogistics")
def test_aggregation_delivery_services(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          connection_settings=app.settings.psb_logistics
                                                          (aggregation=True),
                                                          moderation_settings=admin.moderation.psb_logistics)


def test_offers(app, shop_id, warehouse_id):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                    types="DeliveryPoint", delivery_service_code="PsbLogistics",
                                    expected_value=["DeliveryPoint"])


@allure.description("Создание DeliveryPoint заказа по СД PsbLogistics")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type=payment_type, delivery_type="DeliveryPoint",
                                          service="PsbLogistics", delivery_point_code="1",
                                          shared_data=shared_data["psb_a"]["order_ids"])


# @allure.description("Отмена заказа СД PsbLogistics")
# def test_patch_order_cancelled(app, connections, shared_data):
#     CommonOrders.test_patch_order_cancelled_common(app=app, delivery_service="PsbLogistics",
#                                                    connections=connections,
#                                                    shared_data=shared_data["psb_a"]["order_ids"])


@allure.description("Удаление заказа СД PsbLogistics")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections,
                                          shared_delivery_service="psb_a", shared_data=shared_data)
