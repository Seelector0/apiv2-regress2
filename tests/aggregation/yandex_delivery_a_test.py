import pytest
import allure
from random import randrange
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels
from utils.environment import ENV_OBJECT


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_id(app, connections, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД YandexDelivery")
def test_aggregation_delivery_services(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          delivery_service="YandexDelivery",
                                                          connection_settings=app.settings.yandex_delivery(
                                                              aggregation=True),
                                                          update_settings=admin.dicts.form_settings_ds_yd(),
                                                          moderation_settings=admin.moderation.yandex_delivery)


@allure.description("Получение списка ПВЗ СД YandexDelivery")
def test_delivery_service_points(app, shop_id):
    app.tests_info.test_delivery_service_points_common(shop_id=shop_id, delivery_service_code="YandexDelivery")


@allure.description("Получение оферов по СД YandexDelivery")
@pytest.mark.parametrize("offer_type, payment_type, intake_point_number",
                         [("Courier", "Paid", "6fd48c50-b666-4756-aece-6c11cc34f58b"),
                          ("Courier", "PayOnDelivery", None),
                          ("DeliveryPoint", "Paid", None),
                          ("DeliveryPoint", "PayOnDelivery", "6fd48c50-b666-4756-aece-6c11cc34f58b")])
def test_offers(app, shop_id, warehouse_id, offer_type, payment_type, intake_point_number):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types=offer_type, delivery_service_code="YandexDelivery",
                                    intake_point_number=intake_point_number, expected_value=[f"{offer_type}"])


@allure.description("Создание многоместного заказа по CД YandexDelivery")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "6d93897c-9e8b-4284-8eef-32cd23a94b16"),
                          ("PayOnDelivery", "DeliveryPoint", "6d93897c-9e8b-4284-8eef-32cd23a94b16")])
def test_create_multi_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code,
                            connections, shared_data):
    if payment_type == "PayOnDelivery" and delivery_type == "Courier" and ENV_OBJECT.db_connections() == "metaship":
        pytest.xfail("Тест только для dev стенда")
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                         payment_type=payment_type, delivery_type=delivery_type,
                                         service="YandexDelivery", delivery_point_code=delivery_point_code,
                                         delivery_sum=0, shared_data=shared_data["yandex_delivery_a"]["order_ids"])


@allure.description("Создание заказа по CД YandexDelivery")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code, intake_point_code",
                         [("Paid", "Courier", None, "6fd48c50-b666-4756-aece-6c11cc34f58b"),
                          ("PayOnDelivery", "Courier", None, None),
                          ("Paid", "DeliveryPoint", "6d93897c-9e8b-4284-8eef-32cd23a94b16", None),
                          ("PayOnDelivery", "DeliveryPoint", "6d93897c-9e8b-4284-8eef-32cd23a94b16",
                           "6fd48c50-b666-4756-aece-6c11cc34f58b")])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code,
                             intake_point_code, connections, shared_data):
    if payment_type == "PayOnDelivery" and delivery_type == "Courier" and ENV_OBJECT.db_connections() == "metaship":
        pytest.xfail("Тест только для dev стенда")
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          shop_barcode=f"{randrange(100000000, 999999999)}",
                                          payment_type=payment_type, delivery_type=delivery_type,
                                          service="YandexDelivery", delivery_point_code=delivery_point_code,
                                          intake_point_code=intake_point_code, delivery_sum=0,
                                          shared_data=shared_data["yandex_delivery_a"]["order_ids"])


@allure.description("Получение списка заказов CД YandexDelivery")
def test_get_orders(app, shared_data):
    CommonOrders.test_get_orders_common(app=app, shared_delivery_service="yandex_delivery_a", shared_data=shared_data)


@allure.description("Получение информации о заказе CД YandexDelivery")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["yandex_delivery_a"]["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД YandexDelivery")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["yandex_delivery_a"]["order_ids"])


@allure.description("Получения этикеток CД YandexDelivery вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, 
                                                      shared_data=shared_data["yandex_delivery_a"]["order_ids"])


@allure.description("Получение подробной информации о заказе СД YandexDelivery")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["yandex_delivery_a"]["order_ids"])


@allure.description("Отмена заказа СД YandexDelivery")
def test_patch_order_cancelled(app, connections, shared_data):
    CommonOrders.test_patch_order_cancelled_common(app=app, delivery_service="yandex_delivery_a",
                                                   connections=connections,
                                                   shared_data=shared_data["yandex_delivery_a"]["order_ids"])


@allure.description("Удаление заказа СД YandexDelivery")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections,
                                          shared_delivery_service="yandex_delivery_a", shared_data=shared_data)


@allure.description("Создание партии CД YandexDelivery")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_delivery_service="yandex_delivery_a", shared_data=shared_data)


@allure.description("Получение списка партий CД YandexDelivery")
def test_get_parcels(app, shared_data):
    CommonParcels.test_get_parcels_common(app=app, shared_delivery_service="yandex_delivery_a", shared_data=shared_data)


@allure.description("Получение информации о партии CД YandexDelivery")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data["yandex_delivery_a"]["parcel_ids"])


@allure.description("Получение этикеток СД YandexDelivery")
def test_get_labels(app, shared_data):
    CommonParcels.test_get_label_common(app=app,
                                        shared_data=shared_data["yandex_delivery_a"]["order_ids_in_parcel"])


@allure.description("Получение АПП CД YandexDelivery")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data["yandex_delivery_a"]["parcel_ids"])


@allure.description("Получение документов CД YandexDelivery")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data["yandex_delivery_a"]["parcel_ids"])


@allure.description("Создание формы с этикетками партии СД YandexDelivery")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data["yandex_delivery_a"]["parcel_ids"])
