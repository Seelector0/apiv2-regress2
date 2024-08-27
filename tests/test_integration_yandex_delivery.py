import pytest
import allure
from random import randrange, randint
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels


@allure.description("Подключение настроек службы доставки СД YandexDelivery")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.yandex_delivery())


@allure.description("Получение оферов по СД YandexDelivery")
@pytest.mark.parametrize("offer_type, payment_type", [("Courier", "Paid"), ("Courier", "PayOnDelivery"),
                                                      ("DeliveryPoint", "Paid"), ("DeliveryPoint", "PayOnDelivery")])
def test_offers(app, shop_id, warehouse_id, offer_type, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types=offer_type, delivery_service_code="YandexDelivery",
                                    expected_value=[f"{offer_type}"])


@allure.description("Создание многоместного заказа по CД YandexDelivery")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "6d93897c-9e8b-4284-8eef-32cd23a94b16"),
                          ("PayOnDelivery", "DeliveryPoint", "6d93897c-9e8b-4284-8eef-32cd23a94b16")])
def test_create_multi_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code,
                            connections, shared_data):
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                         payment_type=payment_type, delivery_type=delivery_type,
                                         service="YandexDelivery", delivery_point_code=delivery_point_code,
                                         delivery_sum=0, dimension=app.dicts.dimension(length=randint(1, 4),
                                                                                       width=randint(1, 4),
                                                                                       height=randint(1, 4)),
                                         shared_data=shared_data["order_ids"])


@allure.description("Создание Courier заказа по CД YandexDelivery")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "6d93897c-9e8b-4284-8eef-32cd23a94b16"),
                          ("PayOnDelivery", "DeliveryPoint", "6d93897c-9e8b-4284-8eef-32cd23a94b16")])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code,
                             connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          shop_barcode=f"{randrange(100000000, 999999999)}",
                                          payment_type=payment_type, delivery_type=delivery_type,
                                          service="YandexDelivery", delivery_point_code=delivery_point_code,
                                          delivery_sum=0, length=randint(1, 4), width=randint(1, 4),
                                          height=randint(1, 4), shared_data=shared_data["order_ids"])


@allure.description("Получение списка заказов CД YandexDelivery")
def test_get_orders(app):
    CommonOrders.test_get_orders_common(app=app)


@allure.description("Получение информации о заказе CД YandexDelivery")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД YandexDelivery")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получения этикеток CД YandexDelivery вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, labels, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, labels=labels, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе СД YandexDelivery")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии CД YandexDelivery")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение списка партий CД YandexDelivery")
def test_get_parcels(app):
    CommonParcels.test_get_parcels_common(app=app)


@allure.description("Получение информации о партии CД YandexDelivery")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Получение этикеток СД YandexDelivery")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels(app, labels, shared_data):
    CommonParcels.test_get_label_common(app=app, labels=labels, shared_data=shared_data)


@allure.description("Получение АПП CД YandexDelivery")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов CД YandexDelivery")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД YandexDelivery")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)
