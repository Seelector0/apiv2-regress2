import pytest
import allure
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels


@allure.description("Подключение настроек службы доставки СД Boxberry")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.boxberry())


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.not_parallel
def test_offers_format_widget(app, shop_id, warehouse_id):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, format_="widget",
                                    delivery_service_code="Boxberry")


@allure.description("Получение оферов по СД Boxberry")
@pytest.mark.parametrize("offer_type, payment_type", [("Courier", "Paid"), ("Courier", "PayOnDelivery"),
                                                      ("DeliveryPoint", "Paid"), ("DeliveryPoint", "PayOnDelivery")])
def test_offers(app, shop_id, warehouse_id, offer_type, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types=offer_type, delivery_service_code="Boxberry",
                                    expected_value=[f"{offer_type}"])


@allure.description("Создание многоместного заказа по CД Boxberry")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "77717"),
                          ("PayOnDelivery", "DeliveryPoint", "77717")])
def test_create_multi_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code,
                            connections, shared_data):
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                         payment_type=payment_type, delivery_type=delivery_type, service="Boxberry",
                                         delivery_point_code=delivery_point_code, barcode_1=None, barcode_2=None,
                                         shared_data=shared_data["order_ids"])


@allure.description("Создание заказа по CД Boxberry")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "77717"),
                          ("PayOnDelivery", "DeliveryPoint", "77717")])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code,
                             connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type=payment_type, delivery_type=delivery_type, service="Boxberry",
                                          delivery_point_code=delivery_point_code,
                                          shared_data=shared_data["order_ids"])


@pytest.mark.flaky(reruns=3, reruns_delay=2)
@allure.description("Создание заказа из файла СД Boxberry")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, shop_id, warehouse_id, file_extension, connections, shared_data):
    CommonOrders.test_create_order_from_file_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id,
                                                    connections=connections, code="boxberry",
                                                    shared_data=shared_data["order_ids"],
                                                    file_extension=file_extension)


@allure.description("Получение списка заказов CД Boxberry")
def test_get_orders(app, shared_data):
    CommonOrders.test_get_orders_common(app=app, shared_data=shared_data)


@allure.description("Получение информации о заказе CД Boxberry")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Редактирование веса в заказе СД Boxberry")
def test_patch_order_weight(app, connections, shared_data):
    CommonOrders.test_patch_order_weight_common(app=app, connections=connections,
                                                shared_data=shared_data["order_ids"])


@allure.description("Удаление заказа CД Boxberry")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получения этикетки Boxberry вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, labels, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, labels=labels, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа CД Boxberry")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе CД Boxberry")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии CД Boxberry")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение списка партий CД Boxberry")
def test_get_parcels(app, shared_data):
    CommonParcels.test_get_parcels_common(app=app, shared_data=shared_data)


@allure.description("Получение информации о партии CД Boxberry")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Получение этикетки CД Boxberry")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_label(app, labels, shared_data):
    CommonParcels.test_get_label_common(app=app, labels=labels, shared_data=shared_data)


@allure.description("Получение этикеток заказов из партии СД Boxberry")
def test_get_labels_from_parcel(app, shared_data):
    CommonParcels.test_get_labels_from_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП CД Boxberry")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов CД Boxberry")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД Boxberry")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)


@allure.description("Создание забора СД Boxberry")
def test_create_intake(app, shop_id, warehouse_id, connections):
    CommonOrders.test_create_intake_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, connections=connections,
                                           delivery_service="Boxberry")
