from utils.environment import ENV_OBJECT
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels
import pytest
import allure


@allure.description("Подключение настроек службы доставки СД Pecom")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.pecom())


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.not_parallel
def test_offers_format_widget(app, shop_id, warehouse_without_pickup):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_without_pickup, format_="widget",
                                    delivery_service_code="Pecom")


@allure.description("Получение оферов по СД Pecom")
@pytest.mark.parametrize("offer_type, payment_type",
                         [("Courier", "Paid"), ("Courier", "PayOnDelivery"),
                          ("DeliveryPoint", "Paid"), ("DeliveryPoint", "PayOnDelivery")])
def test_offers(app, shop_id, warehouse_without_pickup, offer_type, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_without_pickup,
                                    payment_type=payment_type,
                                    types=offer_type, delivery_service_code="Pecom", expected_value=[f"{offer_type}"])


@allure.description("Создание многоместного заказа по CД Pecom")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "4749f8b8-2a2a-11e9-80ce-00155d713b38"),
                          ("PayOnDelivery", "DeliveryPoint", "4749f8b8-2a2a-11e9-80ce-00155d713b38")])
def test_create_multi_order(app, shop_id, warehouse_without_pickup, payment_type, delivery_type, delivery_point_code,
                            connections, shared_data):
    if payment_type == "PayOnDelivery" and ENV_OBJECT.db_connections() == "metaship":
        pytest.skip("Тест только для dev стенда")
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id,
                                         warehouse_id=warehouse_without_pickup,
                                         payment_type=payment_type, delivery_type=delivery_type, service="Pecom",
                                         tariff="3",
                                         delivery_point_code=delivery_point_code, shared_data=shared_data["order_ids"])


@allure.description("Создание заказа по CД Pecom")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "4749f8b8-2a2a-11e9-80ce-00155d713b38"),
                          ("PayOnDelivery", "DeliveryPoint", "4749f8b8-2a2a-11e9-80ce-00155d713b38")])
def test_create_single_order(app, shop_id, warehouse_without_pickup, payment_type, delivery_type, delivery_point_code,
                             connections, shared_data):
    if payment_type == "PayOnDelivery" and ENV_OBJECT.db_connections() == "metaship":
        pytest.skip("Тест только для dev стенда")
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id,
                                          warehouse_id=warehouse_without_pickup,
                                          payment_type=payment_type, delivery_type=delivery_type, service="Pecom",
                                          tariff="3",
                                          delivery_point_code=delivery_point_code,
                                          shared_data=shared_data["order_ids"])


@allure.description("Получение списка заказов CД Pecom")
def test_get_orders(app, shared_data):
    CommonOrders.test_get_orders_common(app=app, shared_data=shared_data)


@allure.description("Получение информации о заказе CД Pecom")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД Pecom")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Удаление заказа СД Pecom")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получения этикеток CД Pecom вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, labels="termo", shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе СД Pecom")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии СД Pecom")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data, types="order_ids")


@allure.description("Получение списка партий CД Pecom")
def test_get_parcels(app, shared_data):
    CommonParcels.test_get_parcels_common(app=app, shared_data=shared_data)


@allure.description("Получение информации о партии CД Pecom")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД Pecom (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    CommonParcels.add_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получение этикеток СД Pecom")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, labels="termo", shared_data=shared_data)


@allure.description("Получение этикеток заказов из партии СД Pecom")
def test_get_labels_from_parcel(app, shared_data):
    CommonParcels.test_get_labels_from_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП СД Pecom")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД Pecom")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД Pecom")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД Pecom (Удаление заказа)")
def test_remove_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_remove_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)
