from utils.global_enums import INFO
from utils.checking import Checking
from random import choice
import pytest
import allure


@allure.description("Подключение настроек службы доставки СД KazPost")
def test_integration_delivery_services(app, shop_id):
    kaz_post = app.service.post_delivery_service(shop_id=shop_id, delivery_service=app.settings.kaz_post())
    Checking.check_status_code(response=kaz_post, expected_status_code=201)
    Checking.checking_json_key(response=kaz_post, expected_value=INFO.created_entity)


@allure.description("Получение PostOffice оферов по СД KazPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_post_office(app, shop_id, warehouse_id_kz, payment_type):
    offers_delivery_point = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id_kz,
                                                  payment_type=payment_type, types="PostOffice",
                                                  delivery_service_code="KazPost", country_code="KZ")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["PostOffice"])


@allure.description("Создание PostOffice заказа по СД KazPost")
@pytest.mark.parametrize("execution_number", range(3))
def test_create_order_post_office(app, shop_id, warehouse_id_kz, execution_number, connections, shared_data):
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id_kz, payment_type="Paid",
                                            type_ds="PostOffice", service="KazPost",
                                            declared_value=500, country_code="KZ")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    order_id = new_order.json()["id"]
    connections.wait_create_order(order_id=order_id)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])
    shared_data["order_ids"].append(order_id)


@allure.description("Получение списка заказов CД KazPost")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД KazPost")
def test_get_order_by_id(app, shared_data):
    random_order = app.order.get_order_id(order_id=choice(shared_data["order_ids"]))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Получение информации об истории изменения статусов заказа СД KazPost")
def test_order_status(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получения этикеток CД KazPost вне партии")
def test_get_label_out_of_parcel(app, shared_data):
    for order_id in shared_data["order_ids"]:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД KazPost")
def test_order_details(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД KazPost")
def test_create_parcel(app, shared_data):
    random_order_id = shared_data["order_ids"].pop()
    create_parcel = app.parcel.post_parcel(value=random_order_id)
    parcel_id = create_parcel.json()[0]["id"]
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")
    shared_data["parcel_ids"].append(parcel_id)
    shared_data["order_ids_in_parcel"].append(random_order_id)


@allure.description("Получение списка партий CД KazPost")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД KazPost")
def test_get_parcel_by_id(app, shared_data):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД KazPost (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    for order in shared_data["order_ids"]:
        random_parcel = choice(shared_data["parcel_ids"])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=random_parcel, op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        shared_data["order_ids_in_parcel"].append(order)
        assert order in connections.get_list_all_orders_in_parcel_for_parcel_id(parcel_id=random_parcel)


@allure.description("Получение этикетки СД KazPost")
def test_get_label(app, shared_data):
    for order_id in shared_data["order_ids_in_parcel"]:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД KazPost")
def test_get_app(app, shared_data):
    acceptance = app.document.get_acceptance(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД KazPost")
def test_get_documents(app, shared_data):
    documents = app.document.get_files(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание формы с этикетками партии СД KazPost")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    forms_labels = app.forms.post_forms(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=forms_labels, expected_status_code=201)
    Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)


@allure.description("Редактирование партии СД KazPost (Удаление заказа из партии)")
def test_remove_order_in_parcel(app, connections, shared_data):
    remove_order = app.parcel.patch_parcel(op="remove", order_id=choice(shared_data["order_ids_in_parcel"]),
                                           parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=remove_order, expected_status_code=200)
    assert remove_order is not connections.get_list_all_orders_in_parcel()
