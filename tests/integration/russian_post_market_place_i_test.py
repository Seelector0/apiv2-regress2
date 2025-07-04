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


@allure.description("Подключение настроек службы доставки СД RussianPostMarketPlace")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.russian_post_market_place())


@pytest.mark.parametrize("offer_type, payment_type", [("Courier", "Paid"), ("PostOffice", "Paid")])
def test_offers(app, shop_id, warehouse_id, offer_type, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types=offer_type, delivery_service_code="RussianPostMarketPlace",
                                    expected_value=[f"{offer_type}"])


@allure.description("Создание Courier заказа по СД RussianPostMarketPlace")
def test_create_order_courier(app, shop_id, warehouse_id, connections):
    CommonOrders.test_single_order_minimal_common(app=app, connections=connections, shop_id=shop_id,
                                                  warehouse_id=warehouse_id,
                                                  payment_type="Paid", delivery_type="Courier",
                                                  service="RussianPostMarketPlace")


@allure.description("Создание PostOffice заказа по СД RussianPostMarketPlace")
def test_create_order_post_office(app, shop_id, warehouse_id, connections):
    CommonOrders.test_single_order_minimal_common(app=app, connections=connections, shop_id=shop_id,
                                                  warehouse_id=warehouse_id,
                                                  payment_type="Paid", delivery_type="PostOffice",
                                                  service="RussianPostMarketPlace")
