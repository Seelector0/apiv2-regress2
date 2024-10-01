import pytest
import allure
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels


@allure.description("Подключение настроек службы доставки СД KazPost")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.kaz_post())


@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_post_office(app, shop_id, warehouse_id_kz, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id_kz, payment_type=payment_type,
                                    types="PostOffice", delivery_service_code="KazPost", country_code="KZ",
                                    expected_value=["PostOffice"])


@allure.description("Создание PostOffice заказа по СД KazPost")
@pytest.mark.parametrize("execution_number", range(3))
def test_create_order_post_office(app, shop_id, warehouse_id_kz, execution_number, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id,
                                          warehouse_id=warehouse_id_kz, payment_type="Paid", delivery_type="PostOffice",
                                          service="KazPost", country_code="KZ",
                                          shared_data=shared_data["order_ids"])


@allure.description("Получение списка заказов CД KazPost")
def test_get_orders(app, shared_data):
    CommonOrders.test_get_orders_common(app=app, shared_data=shared_data)


@allure.description("Получение информации о заказе CД KazPost")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД KazPost")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получения этикеток CД KazPost вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе СД KazPost")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии СД KazPost")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение списка партий CД KazPost")
def test_get_parcels(app, shared_data):
    CommonParcels.test_get_parcels_common(app=app, shared_data=shared_data)


@allure.description("Получение информации о партии CД KazPost")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД KazPost (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    CommonParcels.add_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получение этикетки СД KazPost")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП СД KazPost")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД KazPost")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД KazPost")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД KazPost (Удаление заказа из партии)")
def test_remove_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_remove_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)
