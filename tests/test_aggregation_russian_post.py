import pytest
import allure
from random import choice
from utils.global_enums import INFO
from utils.common_tests import CommonConnections, CommonOffers, CommonInfo, CommonOrders, CommonParcels


def test_aggregation_delivery_services(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          connection_settings=app.settings.russian_post(
                                                              aggregation=True),
                                                          moderation_settings=admin.moderation.russian_post)


@allure.description("Получение списка ПВЗ СД RussianPost")
def test_delivery_service_points(app, shop_id):
    CommonInfo.test_delivery_service_points_common(app=app, shop_id=shop_id, delivery_service_code="RussianPost")


@pytest.mark.parametrize("offer_type, payment_type", [("Courier", "Paid"), ("Courier", "PayOnDelivery"),
                                                      ("DeliveryPoint", "Paid"), ("PostOffice", "Paid"),
                                                      ("PostOffice", "PayOnDelivery")])
def test_offers(app, shop_id, warehouse_id, offer_type, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types=offer_type, delivery_service_code="RussianPost",
                                    expected_value=[f"{offer_type}"])


@allure.description("Создание Courier заказа по СД RussianPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type=payment_type, delivery_type="Courier", service="RussianPost",
                                          tariff=choice(INFO.rp_courier_tariffs), shared_data=shared_data["order_ids"],
                                          shared_data_order_type=shared_data["orders_courier"])


@allure.description("Создание DeliveryPoint(terminal) заказа по СД RussianPost")
def test_create_delivery_point_terminal(app, shop_id, warehouse_id, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type="Paid", delivery_type="DeliveryPoint", service="RussianPost",
                                          delivery_point_code="914841", tariff=INFO.rp_po_tariffs[0],
                                          shared_data=shared_data["order_ids"],
                                          shared_data_order_type=shared_data["orders_terminal"])


@allure.description("Создание DeliveryPoint заказа по СД RussianPost")
def test_create_delivery_point(app, shop_id, warehouse_id, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type="Paid", delivery_type="DeliveryPoint", service="RussianPost",
                                          delivery_point_code="980254", tariff=INFO.rp_dp_tariffs[0],
                                          shared_data=shared_data["order_ids"],
                                          shared_data_order_type=shared_data["orders_delivery_point"])


@allure.description("Создание PostOffice заказа по СД RussianPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_post_office(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type=payment_type, delivery_type="PostOffice", service="RussianPost",
                                          tariff=choice(INFO.rp_po_tariffs), shared_data=shared_data["order_ids"],
                                          shared_data_order_type=shared_data["orders_post_office"])


@allure.description("Редактирование заказа СД RussianPost")
def test_editing_order(app, shared_data):
    CommonOrders.test_editing_order_common(app=app, delivery_service="RussianPost",
                                           shared_data=shared_data["order_ids"])


@allure.description("Редактирование веса в заказе СД RussianPost")
def test_patch_order_weight(app, connections, shared_data):
    CommonOrders.test_patch_order_weight_common(app=app, connections=connections,
                                                shared_data=shared_data["order_ids"])


@allure.description("Создание заказа из файла")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, shop_id, warehouse_id, file_extension, connections, shared_data):
    CommonOrders.test_create_order_from_file_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id,
                                                    connections=connections, code="russian_post",
                                                    shared_data=shared_data["order_ids"],
                                                    file_extension=file_extension)


@allure.description("Создание заказа из файла формата СД RussianPost")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, shop_id, warehouse_id, file_extension, connections, shared_data):
    CommonOrders.test_create_order_from_file_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id,
                                                    connections=connections, shared_data=shared_data["order_ids"],
                                                    file_extension=file_extension)


@allure.description("Удаление заказа СД RussianPost")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, delivery_service="RussianPost", connections=connections,
                                          shared_data=shared_data)


@allure.description("Получение списка заказов CД RussianPost")
def test_get_orders(app):
    CommonOrders.test_get_orders_common(app=app)


@allure.description("Получение информации о заказе CД RussianPost")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД RussianPost")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе СД RussianPost")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии СД RussianPost")
@pytest.mark.parametrize("types", ["orders_courier", "orders_post_office"])
def test_create_parcel(app, shared_data, types):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data, types=types)


@allure.description("Получение списка партий CД RussianPost")
def test_get_parcels(app):
    CommonParcels.test_get_parcels_common(app=app)


@allure.description("Получение информации о партии CД RussianPost")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД RussianPost (Добавление заказов)")
@pytest.mark.parametrize("types", ["orders_courier", "orders_post_office"])
def test_add_order_in_parcel(app, connections, shared_data, types):
    CommonParcels.add_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data, types=types)


@allure.description("Редактирование партии СД RussianPost (Изменение даты отправки партии)")
def test_change_shipment_date(app, shared_data):
    CommonParcels.test_change_shipment_date_common(app=app, shared_data=shared_data)


@allure.description("Получение этикетки СД RussianPost")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП СД RussianPost")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД RussianPost")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД RussianPost")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД RussianPost (Удаление заказа из партии)")
def test_remove_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_remove_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)
