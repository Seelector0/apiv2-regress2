import pytest
import allure
from random import choice, randrange
from utils.dates import tomorrow
from utils.global_enums import INFO
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_id(app, connections, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД Dpd")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.dpd())


@allure.description("Создание Courier заказа по CД Dpd")
def test_create_single_order(app, shop_id, warehouse_id, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          shop_barcode=f"{randrange(100000000, 999999999)}",
                                          payment_type="Paid", delivery_type="Courier", service="Dpd",
                                          tariff=choice(INFO.dpd_ds_tariffs),
                                          date_pickup=str(tomorrow), pickup_time_period="9-18",
                                          shared_data=shared_data["dpd_i"]["order_ids"])


@allure.description("Создание партии СД Dpd")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_delivery_service="dpd_i", shared_data=shared_data,
                                       data=tomorrow)


@allure.description("Получение этикеток СД Dpd")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels(app, labels, shared_data):
    CommonParcels.test_get_label_common(app=app, labels=labels,
                                        shared_data=shared_data["dpd_i"]["order_ids_in_parcel"])


@allure.description("Получения оригинальных этикеток CД Dpd в формате A5, A6")
@pytest.mark.parametrize("format_", ["A5", "A6"])
def test_get_original_labels(app, connections, format_, shared_data):
    CommonParcels.test_get_label_common(app=app, format_=format_,
                                        shared_data=shared_data["dpd_i"]["order_ids_in_parcel"])
