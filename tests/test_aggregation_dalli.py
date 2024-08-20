import pytest
import allure
from utils.dates import today, tomorrow
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonInfo, CommonParcels

@allure.description("Подключение настроек службы доставки СД Dalli")
def test_aggregation_delivery_services(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          connection_settings=app.settings.dalli(aggregation=True),
                                                          moderation_settings=admin.moderation.dalli)


@allure.description("Получения сроков доставки по СД Dalli")
@pytest.mark.parametrize("data, tariff_id", [(tomorrow, "1"), (today, "2"), (tomorrow, "11")])
def test_delivery_time_schedules(app, shop_id, data, tariff_id):
    CommonInfo.test_delivery_time_schedules_common(app=app, shop_id=shop_id, delivery_service_code="Dalli", data=data,
                                                   tariff_id=tariff_id)


@allure.description("Получение Courier оферов по СД Dalli")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers(app, shop_id, warehouse_id, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types="Courier", delivery_service_code="Dalli")


@allure.description("Создание многоместного заказа по CД Dalli")
@pytest.mark.parametrize("payment_type, declared_value,  cod", [("Paid", 0, None), ("PayOnDelivery", 3000, 2100.24)])
def test_create_multi_order(app, shop_id, warehouse_id, payment_type, cod, declared_value, connections, shared_data):
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                         payment_type=payment_type, declared_value=declared_value, cod=cod,
                                         delivery_type="Courier", service="Dalli", tariff="1", data=str(tomorrow),
                                         delivery_time={"from": "18:00", "to": "22:00"},
                                         shared_data=shared_data["order_ids"])


@allure.description("Создание Courier заказа по CД Dalli")
@pytest.mark.parametrize("payment_type, declared_value,  cod", [("Paid", 0, None), ("PayOnDelivery", 3000, 3100.24)])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, cod, declared_value, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type=payment_type, declared_value=declared_value, cod=cod,
                                          delivery_type="Courier", service="Dalli", tariff="1", data=str(tomorrow),
                                          delivery_time={"from": "18:00", "to": "22:00"},
                                          shared_data=shared_data["order_ids"])


@allure.description("Получение списка заказов CД Dalli")
def test_get_orders(app):
    CommonOrders.test_get_orders_common(app=app)


@allure.description("Удаление заказа СД Dalli")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получение информации о заказе CД Dalli")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Редактирование заказа СД Dalli")
def test_editing_order(app, shared_data):
    CommonOrders.test_editing_order_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД Cdek")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получения этикеток CД Dalli вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе СД Dalli")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии СД Dalli")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение списка партий CД Dalli")
def test_get_parcels(app):
    CommonParcels.test_get_parcels_common(app=app)


@allure.description("Получение информации о партии CД Dalli")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД Dalli (Добавление заказов)")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Получение этикеток СД Dalli")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП СД Dalli")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД Dalli")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД Dalli")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)
