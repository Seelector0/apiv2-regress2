import pytest
import allure
from conftest import shared_data
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД TopDelivery")
def test_aggregation_delivery_services(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          connection_settings=app.settings.topdelivery(
                                                              aggregation=True),
                                                          moderation_settings=admin.moderation.topdelivery)


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.not_parallel
def test_offers_format_widget(app, shop_id, warehouse_id):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, format_="widget",
                                    delivery_service_code="TopDelivery")


@allure.description("Получение оферов по TopDelivery")
@pytest.mark.parametrize("offer_type, payment_type", [("Courier", "Paid"), ("Courier", "PayOnDelivery"),
                                                      ("DeliveryPoint", "Paid"), ("DeliveryPoint", "PayOnDelivery")])
def test_offers(app, shop_id, warehouse_id, offer_type, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types=offer_type, delivery_service_code="TopDelivery",
                                    expected_value=[f"{offer_type}"])


@allure.description("Создание многоместного заказа по CД TopDelivery")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "55"),
                          ("PayOnDelivery", "DeliveryPoint", "55")])
def test_create_multi_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code,
                            connections, shared_data):
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                         payment_type=payment_type, delivery_type=delivery_type, service="TopDelivery",
                                         delivery_point_code=delivery_point_code,
                                         shared_data=shared_data["top_delivery_a"]["order_ids"])


@allure.description("Создание  заказа по CД TopDelivery")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "55"),
                          ("PayOnDelivery", "DeliveryPoint", "55")])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code,
                             connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type=payment_type, delivery_type=delivery_type, service="TopDelivery",
                                          delivery_point_code=delivery_point_code,
                                          shared_data=shared_data["top_delivery_a"]["order_ids"])


@allure.description("Создание многоместного заказа из одноместного")
def test_patch_single_order(app, connections, shared_data):
    CommonOrders.test_patch_single_order_common(app=app, connections=connections, delivery_service="TopDelivery",
                                                shared_data=shared_data["top_delivery_a"]["order_ids"])


@pytest.mark.flaky(reruns=3, reruns_delay=2)
@allure.description("Создание заказа из файла СД TopDelivery")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, shop_id, warehouse_id, file_extension, connections, shared_data):
    CommonOrders.test_create_order_from_file_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id,
                                                    connections=connections, code="topdelivery",
                                                    shared_data=shared_data["top_delivery_a"]["order_ids"],
                                                    file_extension=file_extension)


@allure.description("Получение списка заказов CД TopDelivery")
def test_get_orders(app, shared_data):
    CommonOrders.test_get_orders_common(app=app, shared_delivery_service="top_delivery_a", shared_data=shared_data)


@allure.description("Получение информации о заказе CД TopDelivery")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["top_delivery_a"]["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД TopDelivery")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["top_delivery_a"]["order_ids"])


@allure.description("Удаление заказа TopDelivery")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections, shared_delivery_service="top_delivery_a",
                                          shared_data=shared_data)


@allure.description("Получения этикеток СД TopDelivery вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, shared_data=shared_data["top_delivery_a"]["order_ids"])


@allure.description("Получение подробной информации о заказе СД TopDelivery")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["top_delivery_a"]["order_ids"])


@allure.description("Создание партии СД TopDelivery")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_delivery_service="top_delivery_a", shared_data=shared_data)


@allure.description("Получение списка партий CД TopDelivery")
def test_get_parcels(app, shared_data):
    CommonParcels.test_get_parcels_common(app=app, shared_delivery_service="top_delivery_a", shared_data=shared_data)


@allure.description("Получение информации о партии CД Topdelivery")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data["top_delivery_a"]["parcel_ids"])


@allure.description("Получение этикеток СД TopDelivery")
def test_get_labels(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data["top_delivery_a"]["order_ids_in_parcel"])


@allure.description("Получение этикеток заказов из партии СД TopDelivery")
def test_get_labels_from_parcel(app, shared_data):
    CommonParcels.test_get_labels_from_parcel_common(app=app, shared_delivery_service="top_delivery_a",
                                                     shared_data=shared_data)


@allure.description("Получение АПП СД TopDelivery")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data["top_delivery_a"]["parcel_ids"])


@allure.description("Получение документов СД TopDelivery")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data["top_delivery_a"]["parcel_ids"])


@allure.description("Создание формы с этикетками партии СД TopDelivery")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data["top_delivery_a"]["parcel_ids"])
