from utils.global_enums import INFO
from utils.checking import Checking
from random import choice
import datetime
import pytest
import allure


@allure.description("Подключение настроек службы доставки СД Cse по агрегации")
def test_integration_delivery_services(app, shop_id):
    cse = app.service.post_delivery_service(shop_id=shop_id,
                                            delivery_service=app.settings.cse(aggregation=True))
    Checking.check_status_code(response=cse, expected_status_code=201)
    Checking.checking_json_key(response=cse, expected_value=INFO.created_entity)


@allure.description("Модерация СД Cse")
def test_moderation_delivery_services(admin, shop_id):
    moderation = admin.connection.post_connections(delivery_service=admin.moderation.cse(shop_id=shop_id))
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


@allure.description("Получение списка ПВЗ СД Cse")
def test_delivery_service_points(app, shop_id):
    delivery_service_points = app.info.get_delivery_service_points(shop_id=shop_id, delivery_service_code="Cse")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.check_response_is_not_empty(response=delivery_service_points)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="Cse")


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.not_parallel
@pytest.mark.xfail
def test_offers_format_widget(app, shop_id, warehouse_id):
    offers_widget = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, format_="widget")
    Checking.check_status_code(response=offers_widget, expected_status_code=200)
    Checking.check_delivery_services_in_widget_offers(response=offers_widget, delivery_service="Cse")


@allure.description("Получение оферов Courier по СД Cse")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, shop_id, warehouse_id, payment_type):
    offers_courier = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                           types="Courier", delivery_service_code="Cse")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Создание Courier многоместного заказа по CД Cse")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    new_order = app.order.post_multi_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                           type_ds="Courier", service="Cse", tariff="64", declared_value=1500,
                                           dimension=app.dicts.dimension(), date_pickup=f"{datetime.date.today()}")
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


@allure.description("Создание DeliveryPoint многоместного заказа по CД Cse")
def test_create_multi_order_delivery_point(app, shop_id, warehouse_id, connections, shared_data):
    new_order = app.order.post_multi_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                           type_ds="DeliveryPoint", service="Cse",
                                           tariff="64", date_pickup=f"{datetime.date.today()}",
                                           dimension=app.dicts.dimension(),
                                           delivery_point_code="0299ca01-ed73-11e8-80c9-7cd30aebf951",
                                           declared_value=1500)
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


@allure.description("Создание Courier заказа по СД Cse")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                            type_ds="Courier", service="Cse", tariff="64",
                                            date_pickup=f"{datetime.date.today()}", declared_value=500)
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


@allure.description("Создание DeliveryPoint заказа по CД Cse")
def test_create_order_delivery_point(app, shop_id, warehouse_id, connections, shared_data):
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                            type_ds="DeliveryPoint", service="Cse", tariff="64",
                                            date_pickup=f"{datetime.date.today()}", declared_value=500,
                                            delivery_point_code="0299ca01-ed73-11e8-80c9-7cd30aebf951")
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


@allure.description("Получение списка заказов CД Cse")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД Cse")
def test_get_order_by_id(app, shared_data):
    random_order = app.order.get_order_id(order_id=choice(shared_data["order_ids"]))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Получение информации об истории изменения статусов заказа СД Cse")
def test_order_status(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Удаление заказа СД Cse")
def test_delete_order(app, connections, shared_data):
    random_order_id = shared_data["order_ids"].pop()
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=random_order_id,
                                                                               value="deleted"),
                                    two_value=[True])


@allure.description("Получения этикеток CД Cse вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    for order_id in shared_data["order_ids"]:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД Cse")
def test_order_details(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Cse")
def test_create_parcel(app, shared_data):
    random_order_id = shared_data["order_ids"].pop()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    create_parcel = app.parcel.post_parcel(value=random_order_id, data=tomorrow)
    parcel_id = create_parcel.json()[0]["id"]
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")
    shared_data["parcel_ids"].append(parcel_id)
    shared_data["order_ids_in_parcel"].append(random_order_id)


@allure.description("Получение списка партий CД Cse")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД Cse")
def test_get_parcel_by_id(app, shared_data):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД Cse (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    for order in shared_data["order_ids"]:
        random_parcel = choice(shared_data["parcel_ids"])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=random_parcel, op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        shared_data["order_ids_in_parcel"].append(order)
        assert order in connections.get_list_all_orders_in_parcel_for_parcel_id(parcel_id=random_parcel)


@allure.description("Получение этикеток СД Cse")
def test_get_labels(app, shared_data):
    for order_id in shared_data["order_ids_in_parcel"]:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД Cse")
def test_get_app(app, shared_data):
    acceptance = app.document.get_acceptance(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД Cse")
def test_get_documents(app, shared_data):
    documents = app.document.get_files(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание формы с этикетками партии СД Cse")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    forms_labels = app.forms.post_forms(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=forms_labels, expected_status_code=201)
    Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)


@allure.description("Редактирование партии СД Cse (Удаление заказа)")
def test_remove_order_in_parcel(app, connections, shared_data):
    remove_order = app.parcel.patch_parcel(op="remove", order_id=choice(shared_data["order_ids_in_parcel"]),
                                           parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=remove_order, expected_status_code=200)
    assert remove_order is not connections.get_list_all_orders_in_parcel()


@allure.description("Создание забора СД Cse")
def test_create_intake(app, shop_id, warehouse_id, connections):
    new_intake = app.intakes.post_intakes(shop_id=shop_id, warehouse_id=warehouse_id, delivery_service="Cse")
    Checking.check_status_code(response=new_intake, expected_status_code=201)
    Checking.checking_json_key(response=new_intake, expected_value=INFO.created_entity)
    get_new_intake = app.intakes.get_intakes_id(intakes_id=new_intake.json()["id"])
    Checking.check_status_code(response=get_new_intake, expected_status_code=200)
    Checking.check_value_comparison(one_value=connections.get_list_intakes_value(
        intake_id=new_intake.json()["id"], value="status"), two_value=["created"])
