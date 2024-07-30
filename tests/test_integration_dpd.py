import pytest
import allure
from random import choice, randrange
from utils.dates import tomorrow
from utils.global_enums import INFO
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels



def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.dpd())


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.not_parallel
def test_offers_format_widget(app, shop_id, warehouse_id):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, format_="widget",
                                    delivery_service_code="Dpd")


@allure.description("Получение оферов по СД Dpd")
@pytest.mark.parametrize("offer_type, payment_type", [("Courier", "Paid"), ("Courier", "PayOnDelivery"),
                                                      ("DeliveryPoint", "Paid"), ("DeliveryPoint", "PayOnDelivery")])
def test_offers(app, shop_id, warehouse_id, offer_type, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types=offer_type, delivery_service_code="Dpd", expected_value=[f"{offer_type}"])


@allure.description("Создание многоместного заказа по CД Dpd")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "LED"),
                          ("PayOnDelivery", "DeliveryPoint", "LED")])
def test_create_multi_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code, connections,
                            shared_data):
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                         payment_type=payment_type, delivery_type=delivery_type, service="Dpd",
                                         tariff=choice(INFO.dpd_ds_tariffs), delivery_point_code=delivery_point_code,
                                         date_pickup=str(tomorrow), pickup_time_period="9-18",
                                         shared_data=shared_data["order_ids"])


@allure.description("Создание одноместного заказа из многоместного СД Dpd")
def test_patch_add_single_order_from_multi_order(app, connections, shared_data):
    CommonOrders.test_patch_add_single_order_from_multi_order_common(app=app, connections=connections,
                                                                     shared_data=shared_data["order_ids"])


@allure.description("Добавление items в многоместный или одноместный заказ СД Dpd")
def test_patch_multi_order(app, connections, shared_data):
    CommonOrders.test_patch_multi_order_common(app=app, connections=connections, shared_data=shared_data["order_ids"])


@allure.description("Создание Courier заказа по CД Dpd")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "LED"),
                          ("PayOnDelivery", "DeliveryPoint", "LED")])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code, connections,
                             shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          shop_barcode=f"{randrange(100000000, 999999999)}",
                                          payment_type=payment_type, delivery_type=delivery_type, service="Dpd",
                                          tariff=choice(INFO.dpd_ds_tariffs),
                                          delivery_point_code=delivery_point_code,
                                          date_pickup=str(tomorrow), pickup_time_period="9-18",
                                          shared_data=shared_data["order_ids"])


@allure.description("Получение списка заказов CД Dpd")
def test_get_orders(app):
    CommonOrders.test_get_orders_common(app=app)


@allure.description("Получение информации о заказе CД Dpd")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД Dpd")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Редактирование веса в заказе СД Dpd")
def test_patch_order_weight(app, connections, shared_data):
    CommonOrders.test_patch_order_weight_common(app=app, connections=connections,
                                                shared_data=shared_data["order_ids"])


@allure.description("Удаление заказа СД Dpd")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получения этикеток CД Dpd вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, labels, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, labels=labels, shared_data=shared_data["order_ids"])


@allure.description("Получения оригинальных этикеток CД Dpd в формате A5, A6 вне партии")
@pytest.mark.parametrize("format_", ["A5", "A6"])
def test_get_original_labels_out_of_parcel(app, shared_data, format_):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, format_=format_, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе СД Dpd")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии СД Dpd")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data,
                                       data=tomorrow)


@allure.description("Получение списка партий CД Dpd")
def test_get_parcels(app):
    CommonParcels.test_get_parcels_common(app=app)


@allure.description("Получение информации о партии CД Dpd")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД Dpd (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    CommonParcels.add_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Редактирование веса заказа в партии СД Dpd")
def test_patch_weight_random_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_patch_weight_random_order_in_parcel_common(app=app, connections=connections,
                                                                  shared_data=shared_data)


@allure.description("Получение этикеток СД Dpd")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels(app, labels, shared_data):
    CommonParcels.test_get_label_common(app=app, labels=labels, shared_data=shared_data)


@allure.description("Получения оригинальных этикеток CД Dpd в формате A5, A6")
@pytest.mark.parametrize("format_", ["A5", "A6"])
def test_get_original_labels(app, connections, format_, shared_data):
    CommonParcels.test_get_label_common(app=app, format_=format_, shared_data=shared_data)


@allure.description("Получение АПП СД Dpd")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД Dpd")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД Dpd")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД Dpd (Удаление заказа)")
def test_remove_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_remove_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)
