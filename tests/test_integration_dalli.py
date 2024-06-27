from utils.global_enums import INFO
from utils.checking import Checking
from random import choice, randrange
import datetime
import pytest
import allure


@allure.description("Подключение настроек службы доставки СД Dalli")
def test_integration_delivery_services(app, shop_id):
    dalli = app.service.post_delivery_service(shop_id=shop_id, delivery_service=app.settings.dalli())
    Checking.check_status_code(response=dalli, expected_status_code=201)
    Checking.checking_json_key(response=dalli, expected_value=INFO.created_entity)


@allure.description("Получения сроков доставки по СД Dalli")
@pytest.mark.parametrize("tariff_id", ["1", "2", "11"])
def test_delivery_time_schedules(app, shop_id, tariff_id):
    delivery_time_schedules = app.info.get_delivery_time_schedules(shop_id=shop_id, delivery_service_code="Dalli",
                                                                   tariff_id=tariff_id)
    Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
    if tariff_id == "1":
        Checking.checking_json_value(response=delivery_time_schedules, key_name="intervals",
                                     expected_value=INFO.dalli_intervals_1)
    elif tariff_id == "2":
        Checking.checking_json_value(response=delivery_time_schedules, key_name="intervals",
                                     expected_value=INFO.dalli_intervals_2)
    elif tariff_id == "11":
        Checking.checking_json_value(response=delivery_time_schedules, key_name="intervals",
                                     expected_value=INFO.dalli_intervals_11)


@allure.description("Получение Courier оферов по СД Dalli")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, shop_id, warehouse_id, payment_type):
    offers_courier = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                           types="Courier", delivery_service_code="Dalli")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Создание Courier многоместного заказа по CД Dalli")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    if payment_type == "PayOnDelivery":
        new_order = app.order.post_multi_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                               type_ds="Courier", service="Dalli", data=str(tomorrow), tariff="1",
                                               declared_value=0, delivery_time={"from": "18:00", "to": "22:00"},
                                               barcode_1=f"{randrange(1000000, 9999999)}",
                                               barcode_2=f"{randrange(1000000, 9999999)}", cod=2100.24)
    else:
        new_order = app.order.post_multi_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                               type_ds="Courier", service="Dalli", data=str(tomorrow), tariff="1",
                                               declared_value=0, delivery_time={"from": "18:00", "to": "22:00"},
                                               barcode_1=f"{randrange(1000000, 9999999)}",
                                               barcode_2=f"{randrange(1000000, 9999999)}")
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


@allure.description("Создание Courier заказа по CД Dalli")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    if payment_type == "PayOnDelivery":
        new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                                type_ds="Courier", service="Dalli", cod=3100.24, data=str(tomorrow),
                                                tariff="1", declared_value=0, delivery_time={"from": "18:00",
                                                                                             "to": "22:00"})
    else:
        new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                                type_ds="Courier", service="Dalli", data=str(tomorrow), tariff="1",
                                                declared_value=3000, delivery_time={"from": "18:00", "to": "22:00"})
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


@allure.description("Получение списка заказов CД Dalli")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Удаление заказа СД Dalli")
def test_delete_order(app, connections, shared_data):
    random_order_id = shared_data["order_ids"].pop()
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=random_order_id,
                                                                               value="deleted"),
                                    two_value=[True])


@allure.description("Получение информации о заказе CД Dalli")
def test_get_order_by_id(app, shared_data):
    random_order = app.order.get_order_id(order_id=choice(shared_data["order_ids"]))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Редактирование заказа СД Dalli")
def test_editing_order(app, shared_data):
    random_order = choice(shared_data["order_ids"])
    order_put = app.order.put_order(order_id=random_order, weight=5, length=12, width=14, height=11,
                                    family_name="Иванов")
    Checking.check_status_code(response=order_put, expected_status_code=200)
    Checking.checking_big_json(response=order_put, key_name="weight", expected_value=5)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="length", expected_value=12)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="width", expected_value=14)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="height", expected_value=11)
    Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName", expected_value="Иванов")


@allure.description("Получение информации об истории изменения статусов заказа СД Dalli")
def test_order_status(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получения этикеток CД Dalli вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, shared_data, labels):
    for order_id in shared_data["order_ids"]:
        label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД Dalli")
def test_order_details(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Dalli")
def test_create_parcel(app, shared_data):
    random_order_id = shared_data["order_ids"].pop()
    create_parcel = app.parcel.post_parcel(value=random_order_id)
    parcel_id = create_parcel.json()[0]["id"]
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")
    shared_data["parcel_ids"].append(parcel_id)
    shared_data["order_ids_in_parcel"].append(random_order_id)


@allure.description("Получение списка партий CД Dalli")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД Dalli")
def test_get_parcel_by_id(app, shared_data):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД Dalli (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    for order in shared_data["order_ids"]:
        random_parcel = choice(shared_data["parcel_ids"])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=random_parcel, op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        shared_data["order_ids_in_parcel"].append(order)
        assert order in connections.get_list_all_orders_in_parcel_for_parcel_id(parcel_id=random_parcel)


@allure.description("Получение этикеток СД Dalli")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_label(app, shared_data, labels):
    for order_id in shared_data["order_ids_in_parcel"]:
        label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД Dalli")
def test_get_app(app, shared_data):
    acceptance = app.document.get_acceptance(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД Dalli")
def test_get_documents(app, shared_data):
    documents = app.document.get_files(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание формы с этикетками партии СД Dalli")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    forms_labels = app.forms.post_forms(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=forms_labels, expected_status_code=201)
    Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)
