import pytest
import allure
from utils.environment import ENV_OBJECT
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels

@allure.description("Подключение настроек службы доставки СД FivePost")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.five_post())


@allure.description("Получение DeliveryPoint оферов по СД FivePost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers(app, shop_id, warehouse_id, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types="DeliveryPoint", delivery_service_code="FivePost",
                                    delivery_point_number="006bf88a-5186-45d9-9911-89d37f1edc86",
                                    expected_value=["DeliveryPoint"])


@allure.description("Создание DeliveryPoint заказа по СД FivePost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type=payment_type, delivery_type="DeliveryPoint", service="FivePost",
                                          delivery_point_code="006bf88a-5186-45d9-9911-89d37f1edc86",
                                          shared_data=shared_data["order_ids"])


@allure.description("Создание заказа из файла СД FivePost")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, shop_id, warehouse_id, file_extension, connections, shared_data):
    CommonOrders.test_create_order_from_file_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id,
                                                    connections=connections, code="five_post",
                                                    shared_data=shared_data["order_ids"],
                                                    file_extension=file_extension)


@allure.description("Получение списка заказов CД FivePost")
def test_get_orders(app):
    CommonOrders.test_get_orders_common(app=app)


@allure.description("Получение информации о заказе CД FivePost")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД FivePost")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Редактирование веса в заказе СД FivePost")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_patch_order_weight(app, connections, shared_data):
    CommonOrders.test_patch_order_weight_common(app=app, connections=connections,
                                                shared_data=shared_data["order_ids"])


@allure.description("Редактирование информации о получателе в заказе СД FivePost")
def test_patch_order_recipient(app, connections, shared_data):
    CommonOrders.patch_order_recipient_common(app=app, connections=connections, shared_data=shared_data["order_ids"])


@allure.description("Редактирование одноместного заказа СД FivePost")
def test_patch_single_order(app, connections, shared_data):
    CommonOrders.test_patch_single_order_common(app=app, delivery_service="FivePost", connections=connections,
                                                shared_data=shared_data["order_ids"])


@allure.description("Получение кода выдачи заказа для СД FivePost")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_generate_security_code(app, shared_data):
    CommonOrders.test_generate_security_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Удаление заказа СД FivePost")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получения этикетки СД FivePost вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе СД FivePost")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии СД FivePost")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение списка партий CД FivePost")
def test_get_parcels(app):
    CommonParcels.test_get_parcels_common(app=app)


@allure.description("Получение информации о партии CД FivePost")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД FivePost (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    CommonParcels.add_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Редактирование веса заказа в партии СД FivePost")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_patch_weight_random_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_patch_weight_random_order_in_parcel_common(app=app, connections=connections,
                                                                  shared_data=shared_data)


@allure.description("Получение этикеток СД FivePost")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data)


@allure.description("Получение этикеток заказов из партии СД FivePost")
def test_get_labels_from_parcel(app, shared_data):
    CommonParcels.test_get_labels_from_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП СД FivePost")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД FivePost")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД FivePost")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД FivePost (Удаление заказа)")
def test_remove_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_remove_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)
