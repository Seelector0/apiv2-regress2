from utils.global_enums import INFO
from utils.checking import Checking
from random import randrange, choice
import datetime
import pytest
import allure


@allure.description("Создание магазина")
def test_create_shop(app, connections):
    if len(connections.get_list_shops()) == 0:
        app.tests_shop.post_shop()


@allure.description("Создание склада")
def test_create_warehouse(app, connections):
    if len(connections.get_list_warehouses()) == 0:
        app.tests_warehouse.post_warehouse()


@allure.description("Подключение настроек службы доставки СД DostavkaGuru")
def test_integration_delivery_services(app):
    guru = app.service.post_delivery_service(delivery_service=app.settings.dostavka_guru())
    Checking.check_status_code(response=guru, expected_status_code=201)
    Checking.checking_json_key(response=guru, expected_value=INFO.created_entity)


@allure.description("Создание Courier заказа по CД DostavkaGuru")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, payment_type, connections):
    day = datetime.date.today() + datetime.timedelta(days=2)
    new_order = app.order.post_single_order(payment_type=payment_type, type_ds="Courier", service="DostavkaGuru",
                                            declared_value=500, data=f"{day}", routes=[
                                                    {
                                                        "deliveryService": "RussianPost",
                                                        "deferred": True
                                                    }
                                            ], items_declared_value=1000, shop_barcode=f"{randrange(1000000, 9999999)}")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=["id", "type", "url", "status"])
    connections.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])


@allure.description("Получение списка заказов CД DostavkaGuru")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД DostavkaGuru")
def test_get_order_by_id(app, connections):
    random_order = app.order.get_order_id(order_id=choice(connections.get_list_all_orders_out_parcel()))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Получение информации об истории изменения статусов заказа СД DostavkaGuru")
def test_order_status(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получения этикеток CД DostavkaGuru вне партии")
def test_get_labels_out_of_parcel(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        label = app.document.get_label(order_id=order_id, type_="termo")
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе CД DostavkaGuru")
def test_order_details(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии CД DostavkaGuru")
def test_create_parcel(app, connections):
    create_parcel = app.parcel.post_parcel(value=connections.get_list_all_orders_out_parcel())
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение списка партий CД DostavkaGuru")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД DostavkaGuru")
def test_get_parcel_by_id(app, connections):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(connections.get_list_parcels()))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Получение этикеток СД DostavkaGuru")
def test_get_label(app, connections):
    for order_id in (connections.get_list_all_orders_in_parcel()):
        label = app.document.get_label(order_id=order_id, type_="termo")
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД DostavkaGuru")
def test_get_labels_from_parcel(app, connections):
    labels_from_parcel = app.document.post_labels(order_ids=connections.get_list_all_orders_in_parcel())
    Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП СД DostavkaGuru")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД DostavkaGuru")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание формы с этикетками партии СД DostavkaGuru")
def test_forms_parcels_labels(app):
    forms_labels = app.forms.post_forms()
    Checking.check_status_code(response=forms_labels, expected_status_code=201)
    Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)
