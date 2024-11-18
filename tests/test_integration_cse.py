import pytest
import allure
from utils.dates import today
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_without_pickup(app, connections, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(pickup=False, warehouse_type="warehouse_without_pickup",
                                              shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД Cse")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.cse())


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.not_parallel
def test_offers_format_widget(app, shop_id, warehouse_without_pickup):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_without_pickup, format_="widget",
                                    delivery_service_code="Cse")


@allure.description("Получение оферов по СД Cse")
@pytest.mark.parametrize("offer_type, payment_type",
                         [("Courier", "Paid"), ("Courier", "PayOnDelivery"),
                          ("DeliveryPoint", "Paid"), ("DeliveryPoint", "PayOnDelivery")])
def test_offers(app, shop_id, warehouse_without_pickup, offer_type, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_without_pickup,
                                    payment_type=payment_type,
                                    types=offer_type, delivery_service_code="Cse", expected_value=[f"{offer_type}"])


@allure.description("Создание многоместного заказа по CД Cse")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "0299ca01-ed73-11e8-80c9-7cd30aebf951"),
                          ("PayOnDelivery", "DeliveryPoint", "0299ca01-ed73-11e8-80c9-7cd30aebf951")])
def test_create_multi_order(app, shop_id, warehouse_without_pickup, payment_type, delivery_type, delivery_point_code,
                            connections, shared_data):
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id,
                                         warehouse_id=warehouse_without_pickup,
                                         payment_type=payment_type, delivery_type=delivery_type, service="Cse",
                                         tariff="64", delivery_point_code=delivery_point_code,
                                         date_pickup=str(today), shared_data=shared_data["cse_i"]["order_ids"])


@allure.description("Создание заказа по СД Cse")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "0299ca01-ed73-11e8-80c9-7cd30aebf951"),
                          ("PayOnDelivery", "DeliveryPoint", "0299ca01-ed73-11e8-80c9-7cd30aebf951")])
def test_create_single_order(app, shop_id, warehouse_without_pickup, payment_type, delivery_type, delivery_point_code,
                             connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id,
                                          warehouse_id=warehouse_without_pickup,
                                          payment_type=payment_type, delivery_type=delivery_type, service="Cse",
                                          tariff="64", delivery_point_code=delivery_point_code,
                                          date_pickup=str(today),
                                          shared_data=shared_data["cse_i"]["order_ids"])


@allure.description("Получение списка заказов CД Cse")
def test_get_orders(app, shared_data):
    CommonOrders.test_get_orders_common(app=app, shared_delivery_service="cse_i", shared_data=shared_data)


@allure.description("Получение информации о заказе CД Cse")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["cse_i"]["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД Cse")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["cse_i"]["order_ids"])


@allure.description("Удаление заказа СД Cse")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections, shared_delivery_service="cse_i",
                                          shared_data=shared_data)


@allure.description("Получения этикеток CД Cse вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, labels, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, labels=labels,
                                                      shared_data=shared_data["cse_i"]["order_ids"])


@allure.description("Получение подробной информации о заказе СД Cse")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["cse_i"]["order_ids"])


@allure.description("Создание партии СД Cse")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_delivery_service="cse_i", shared_data=shared_data)


@allure.description("Получение списка партий CД Cse")
def test_get_parcels(app, shared_data):
    CommonParcels.test_get_parcels_common(app=app, shared_delivery_service="cse_i", shared_data=shared_data)


@allure.description("Получение информации о партии CД Cse")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data["cse_i"]["parcel_ids"])


@allure.description("Редактирование партии СД Cse (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    CommonParcels.add_order_in_parcel_common(app=app, connections=connections, shared_delivery_service="cse_i",
                                             shared_data=shared_data)


@allure.description("Получение этикеток СД Cse")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels(app, labels, shared_data):
    CommonParcels.test_get_label_common(app=app, labels=labels,
                                        shared_data=shared_data["cse_i"]["order_ids_in_parcel"])


@allure.description("Получение АПП СД Cse")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data["cse_i"]["parcel_ids"])


@allure.description("Получение документов СД Cse")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data["cse_i"]["parcel_ids"])


@allure.description("Создание формы с этикетками партии СД Cse")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data["cse_i"]["parcel_ids"])


@allure.description("Редактирование партии СД Cse (Удаление заказа)")
def test_remove_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_remove_order_in_parcel_common(app=app, connections=connections, shared_delivery_service="cse_i",
                                                     shared_data=shared_data)


@allure.description("Создание забора СД Cse")
def test_create_intake(app, shop_id, warehouse_without_pickup, connections):
    CommonOrders.test_create_intake_common(app=app, shop_id=shop_id, warehouse_id=warehouse_without_pickup,
                                           connections=connections,
                                           delivery_service="Cse")
