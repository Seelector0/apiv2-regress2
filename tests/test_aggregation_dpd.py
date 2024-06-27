from random import choice, randrange
from utils.global_enums import INFO
from utils.checking import Checking
import datetime
import pytest
import allure


@allure.description("Подключение настроек службы доставки СД Dpd по агрегации")
def test_integration_delivery_services(app, shop_id):
    dpd = app.service.post_delivery_service(shop_id=shop_id, delivery_service=app.settings.dpd(aggregation=True))
    Checking.check_status_code(response=dpd, expected_status_code=201)
    Checking.checking_json_key(response=dpd, expected_value=INFO.created_entity)


@allure.description("Модерация СД Dpd")
def test_moderation_delivery_services(admin, shop_id):
    moderation = admin.connection.post_connections(delivery_service=admin.moderation.dpd(shop_id=shop_id))
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


@allure.description("Получение списка ПВЗ СД Dpd")
def test_delivery_service_points(app, shop_id):
    delivery_service_points = app.info.get_delivery_service_points(shop_id=shop_id, delivery_service_code="Dpd")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.check_response_is_not_empty(response=delivery_service_points)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="Dpd")


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.not_parallel
def test_offers_format_widget(app, shop_id, warehouse_id):
    offers_widget = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, format_="widget")
    Checking.check_status_code(response=offers_widget, expected_status_code=200)
    Checking.check_delivery_services_in_widget_offers(response=offers_widget, delivery_service="Dpd")


@allure.description("Получение Courier оферов по СД Dpd")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, shop_id, warehouse_id, payment_type):
    offers_courier = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                           types="Courier", delivery_service_code="Dpd")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Получение DeliveryPoint оферов по СД Dpd")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, shop_id, warehouse_id, payment_type):
    offers_delivery_point = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                                  types="DeliveryPoint", delivery_service_code="Dpd")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание Courier многоместного заказа по CД Dpd")
def test_create_multi_order_courier(app, shop_id, warehouse_id, connections, shared_data):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    new_order = app.order.post_multi_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                           type_ds="Courier", service="Dpd", tariff=choice(INFO.dpd_courier_tariffs),
                                           date_pickup=f"{tomorrow}", pickup_time_period="9-18", declared_value=500,
                                           barcode_1=f"{randrange(1000000, 9999999)}",
                                           barcode_2=f"{randrange(1000000, 9999999)}")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    order_id = new_order.json()["id"]
    connections.wait_create_order(order_id=order_id)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order_id,
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order_id,
                                                                               value="state"),
                                    two_value=["succeeded"])
    shared_data["order_ids"].append(order_id)


@allure.description("Создание DeliveryPoint многоместного заказа по CД Dpd")
def test_create_multi_order_delivery_point(app, shop_id, warehouse_id, connections, shared_data):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    new_order = app.order.post_multi_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                           type_ds="DeliveryPoint", service="Dpd", tariff=choice(INFO.dpd_ds_tariffs),
                                           date_pickup=f"{tomorrow}",
                                           pickup_time_period="9-18", delivery_point_code="LED",
                                           declared_value=500, barcode_1=f"{randrange(1000000, 9999999)}",
                                           barcode_2=f"{randrange(1000000, 9999999)}")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    order_id = new_order.json()["id"]
    connections.wait_create_order(order_id=order_id)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order_id,
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order_id,
                                                                               value="state"),
                                    two_value=["succeeded"])
    shared_data["order_ids"].append(order_id)


@allure.description("Создание одноместного заказа из многоместного СД Dpd")
def test_patch_add_single_order_from_multi_order(app, shared_data):
    random_order_id = choice(shared_data["order_ids"])
    multi_order = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=multi_order, expected_status_code=200)
    patch_multi_order = app.order.patch_order(order_id=random_order_id, name="Пуфик", price=500, count=2, weight=2,
                                              barcode=f"{randrange(1000000, 9999999)}")
    Checking.check_status_code(response=patch_multi_order, expected_status_code=200)
    Checking.checking_json_value(response=patch_multi_order, key_name="status", expected_value="created")
    Checking.checking_json_value(response=patch_multi_order, key_name="state", expected_value="succeeded")
    assert len(multi_order.json()["data"]["request"]["places"]) > \
           len(patch_multi_order.json()["data"]["request"]["places"])


@allure.description("Добавление items в многоместный или одноместный заказ СД Dpd")
def test_patch_multi_order(app, shared_data):
    choice_order_id = choice(shared_data["order_ids"])
    old_len_order_list = app.order.get_order_id(order_id=choice_order_id)
    patch_order = app.order.patch_order_add_item(order_id=choice_order_id)
    Checking.check_status_code(response=patch_order, expected_status_code=200)
    Checking.checking_json_value(response=patch_order, key_name="status", expected_value="created")
    Checking.checking_json_value(response=patch_order, key_name="state", expected_value="succeeded")
    new_len_order_list = app.order.get_order_id(order_id=choice_order_id)
    Checking.check_status_code(response=new_len_order_list, expected_status_code=200)
    Checking.checking_json_value(response=new_len_order_list, key_name="status", expected_value="created")
    Checking.checking_json_value(response=new_len_order_list, key_name="state", expected_value="succeeded")
    Checking.checking_sum_len_lists(old_list=old_len_order_list.json()["data"]["request"]["places"],
                                    new_list=new_len_order_list.json()["data"]["request"]["places"])


@allure.description("Создание Courier заказа по CД Dpd")
def test_create_order_courier(app, shop_id, warehouse_id, connections, shared_data):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                            type_ds="Courier", service="Dpd",
                                            shop_barcode=f"{randrange(100000000, 999999999)}",
                                            tariff=choice(INFO.dpd_courier_tariffs), date_pickup=f"{tomorrow}",
                                            pickup_time_period="9-18", declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    order_id = new_order.json()["id"]
    connections.wait_create_order(order_id=order_id)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order_id,
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order_id,
                                                                               value="state"),
                                    two_value=["succeeded"])
    shared_data["order_ids"].append(order_id)


@allure.description("Создание DeliveryPoint заказа по CД Dpd")
def test_create_order_delivery_point(app, shop_id, warehouse_id, connections, shared_data):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                            type_ds="DeliveryPoint", service="Dpd",
                                            shop_barcode=f"{randrange(100000000, 999999999)}",
                                            tariff=choice(INFO.dpd_ds_tariffs), date_pickup=f"{tomorrow}",
                                            pickup_time_period="9-18", delivery_point_code="LED", declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    order_id = new_order.json()["id"]
    connections.wait_create_order(order_id=order_id)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order_id,
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order_id,
                                                                               value="state"),
                                    two_value=["succeeded"])
    shared_data["order_ids"].append(order_id)


@allure.description("Получение списка заказов CД Dpd")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД Dpd")
def test_get_order_by_id(app, shared_data):
    random_order = app.order.get_order_id(order_id=choice(shared_data["order_ids"]))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Получение информации об истории изменения статусов заказа СД Dpd")
def test_order_status(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Редактирование веса в заказе СД Dpd")
def test_patch_order_weight(app, shared_data):
    random_order = choice(shared_data["order_ids"])
    order_patch = app.order.patch_order_weight(order_id=random_order, weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Удаление заказа СД Dpd")
def test_delete_order(app, connections, shared_data):
    random_order_id = shared_data["order_ids"].pop()
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=random_order_id,
                                                                               value="deleted"),
                                    two_value=[True])


@allure.description("Получения этикеток CД Dpd вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    for order_id in shared_data["order_ids"]:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД Dpd")
def test_order_details(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Dpd")
def test_create_parcel(app, shared_data):
    random_order_id = shared_data["order_ids"].pop()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    create_parcel = app.parcel.post_parcel(value=random_order_id, data=tomorrow)
    parcel_id = create_parcel.json()[0]["id"]
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")
    shared_data["parcel_ids"].append(parcel_id)
    shared_data["order_ids_in_parcel"].append(random_order_id)


@allure.description("Получение списка партий CД Dpd")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД Dpd")
def test_get_parcel_by_id(app, shared_data):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД Dpd (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    for order in shared_data["order_ids"]:
        random_parcel = choice(shared_data["parcel_ids"])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=random_parcel, op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        shared_data["order_ids_in_parcel"].append(order)
        assert order in connections.get_list_all_orders_in_parcel_for_parcel_id(parcel_id=random_parcel)


@allure.description("Редактирование веса заказа в партии СД Dpd")
def test_patch_weight_random_order_in_parcel(app, shared_data):
    order_patch = app.order.patch_order_weight(order_id=choice(shared_data["order_ids_in_parcel"]), weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Получение этикеток СД Dpd")
def test_get_label(app, shared_data):
    for order_id in shared_data["order_ids_in_parcel"]:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД Dpd")
def test_get_app(app, shared_data):
    acceptance = app.document.get_acceptance(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД Dpd")
def test_get_documents(app, shared_data):
    documents = app.document.get_files(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание формы с этикетками партии СД Dpd")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    forms_labels = app.forms.post_forms(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=forms_labels, expected_status_code=201)
    Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)


@allure.description("Редактирование партии СД Dpd (Удаление заказа)")
def test_remove_order_in_parcel(app, connections, shared_data):
    remove_order = app.parcel.patch_parcel(op="remove", order_id=choice(shared_data["order_ids_in_parcel"]),
                                           parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=remove_order, expected_status_code=200)
    assert remove_order is not connections.get_list_all_orders_in_parcel()
