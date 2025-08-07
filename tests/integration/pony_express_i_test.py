import pytest
import allure
from utils.common_tests import CommonConnections, CommonOrders, CommonParcels


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_id_kz(app, connections, shared_data):
    """Фикстура создания склада для Казахстана"""
    return app.tests_warehouse.post_warehouse(country_code="KZ", pickup=True,  warehouse_type="warehouse_id",
                                              shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД PonyExpress")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.pony_express())


@allure.description("Создание Courier заказа по СД PonyExpress")
def test_create_order_courier(app, shop_id, warehouse_id_kz, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id,
                                          warehouse_id=warehouse_id_kz, payment_type="Paid",
                                          delivery_type="Courier", service="PonyExpress", country_code="KZ",
                                          tariff="Express", shared_data=shared_data["pony_express_i"]["order_ids"])


@allure.description("Создание партии СД PonyExpress")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_delivery_service="pony_express_i", shared_data=shared_data)


@allure.description("Получение этикетки СД PonyExpress")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data["pony_express_i"]["order_ids_in_parcel"])
