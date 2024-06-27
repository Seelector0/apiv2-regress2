from utils.environment import ENV_OBJECT
from utils.checking import Checking
from utils.global_enums import INFO
from random import choice
import pytest
import allure

@allure.description("Подключение настроек службы доставки СД DostavkaClub")
def test_integration_delivery_services(app, shop_id):
    club = app.service.post_delivery_service(shop_id=shop_id, delivery_service=app.settings.dostavka_club())
    Checking.check_status_code(response=club, expected_status_code=201)
    Checking.checking_json_key(response=club, expected_value=INFO.created_entity)


@allure.description("Получение оферов Courier по СД DostavkaClub")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, shop_id, warehouse_id, payment_type):
    offers_courier = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                           types="Courier", delivery_service_code="DostavkaClub")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Создание Courier многоместного заказа по CД DostavkaClub")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    new_order = app.order.post_multi_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                           type_ds="Courier", service="DostavkaClub",
                                           tariff=choice(INFO.club_tariffs), declared_value=1500)
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


@allure.description("Добавление items в многоместный заказ СД DostavkaClub")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_patch_multi_order(app, connections, shared_data):
    choice_order_id = choice(shared_data["order_ids"])
    old_len_order_list = app.order.get_order_id(order_id=choice_order_id)
    patch_order = app.order.patch_order_add_item(order_id=choice_order_id)
    Checking.check_status_code(response=patch_order, expected_status_code=200)
    Checking.checking_json_value(response=patch_order, key_name="status", expected_value="created")
    Checking.checking_json_value(response=patch_order, key_name="state", expected_value="succeeded")
    connections.wait_create_order(order_id=choice_order_id)
    new_len_order_list = app.order.get_order_id(order_id=choice_order_id)
    Checking.check_status_code(response=new_len_order_list, expected_status_code=200)
    Checking.checking_json_value(response=new_len_order_list, key_name="status", expected_value="created")
    Checking.checking_json_value(response=new_len_order_list, key_name="state", expected_value="succeeded")
    Checking.checking_sum_len_lists(old_list=old_len_order_list.json()["data"]["request"]["places"],
                                    new_list=new_len_order_list.json()["data"]["request"]["places"])


@allure.description("Создание Courier заказа по CД DostavkaClub")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                            type_ds="Courier", service="DostavkaClub",
                                            tariff=choice(INFO.club_tariffs), declared_value=500)
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


@allure.description("Получение списка заказов CД DostavkaClub")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД DostavkaClub")
def test_get_order_by_id(app, shared_data):
    random_order = app.order.get_order_id(order_id=choice(shared_data["order_ids"]))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Получение информации об истории изменения статусов заказа СД DostavkaClub")
def test_order_status(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе CД DostavkaClub")
def test_order_details(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии CД DostavkaClub")
def test_create_parcel(app, shared_data):
    random_order_id = shared_data["order_ids"].pop()
    create_parcel = app.parcel.post_parcel(value=random_order_id)
    parcel_id = create_parcel.json()[0]["id"]
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")
    shared_data["parcel_ids"].append(parcel_id)
    shared_data["order_ids_in_parcel"].append(random_order_id)


@allure.description("Получение списка партий CД DostavkaClub")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД DostavkaClub")
def test_get_parcel_by_id(app, shared_data):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Получение АПП CД DostavkaClub")
def test_get_app(app,shared_data):
    acceptance = app.document.get_acceptance(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов CД DostavkaClub")
def test_get_documents(app, shared_data):
    documents = app.document.get_files(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание формы с этикетками партии СД DostavkaClub")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    forms_labels = app.forms.post_forms(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=forms_labels, expected_status_code=201)
    Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)
