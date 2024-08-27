import pytest
import allure
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels


@allure.description("Подключение настроек службы доставки СД PonyExpress")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.pony_express())


@allure.description("Получение Courier оферов по СД PonyExpress")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, shop_id, warehouse_id_kz, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id_kz, payment_type=payment_type,
                                    types="Courier", delivery_service_code="PonyExpress", country_code="KZ",
                                    expected_value=["Courier"])


@allure.description("Создание Courier заказа по СД PonyExpress")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, shop_id, warehouse_id_kz, payment_type, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id,
                                          warehouse_id=warehouse_id_kz, payment_type=payment_type,
                                          delivery_type="Courier", service="PonyExpress", country_code="KZ",
                                          tariff="Express", shared_data=shared_data["order_ids"])


@allure.description("Получение списка заказов CД PonyExpress")
def test_get_orders(app):
    CommonOrders.test_get_orders_common(app=app)


@allure.description("Получение информации о заказе CД PonyExpress")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД PonyExpress")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получения этикеток CД PonyExpress вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе СД PonyExpress")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии СД PonyExpress")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение списка партий CД PonyExpress")
def test_get_parcels(app):
    CommonParcels.test_get_parcels_common(app=app)


@allure.description("Получение информации о партии CД PonyExpress")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД PonyExpress (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    CommonParcels.add_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получение этикетки СД PonyExpress")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП СД PonyExpress")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД PonyExpress")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД PonyExpress (Удаление заказа из партии)")
def test_remove_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_remove_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)
