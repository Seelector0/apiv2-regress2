from utils.enums.global_enums import INFO
from utils.checking import Checking
from random import randrange
import datetime
import pytest
import allure


@allure.description("Создание магазина")
def test_create_integration_shop(app):
    new_shop = app.shop.post_shop()
    Checking.check_status_code(response=new_shop, expected_status_code=201)
    Checking.checking_json_key(response=new_shop, expected_value=["id", "type", "url", "status"])
    get_new_shop = app.shop.get_shop_id(shop_id=new_shop.json()["id"])
    Checking.check_status_code(response=get_new_shop, expected_status_code=200)
    Checking.checking_json_value(response=get_new_shop, key_name="visibility", expected_value=True)


@allure.description("Создание склада")
def test_create_warehouse(app):
    new_warehouse = app.warehouse.post_warehouse()
    Checking.check_status_code(response=new_warehouse, expected_status_code=201)
    Checking.checking_json_key(response=new_warehouse, expected_value=["id", "type", "url", "status"])
    get_new_warehouse = app.warehouse.get_warehouse_id(warehouse_id=new_warehouse.json()["id"])
    Checking.check_status_code(response=get_new_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=get_new_warehouse, key_name="visibility", expected_value=True)


@allure.description("Подключение настроек СД DostavkaGuru")
def test_integration_delivery_services(app):
    dostavka_guru = app.service.delivery_services_dostavka_guru()
    Checking.check_status_code(response=dostavka_guru, expected_status_code=201)
    Checking.checking_json_key(response=dostavka_guru, expected_value=["id", "type", "url", "status"])
    get_dostavka_guru = app.service.get_delivery_services_code(code="DostavkaGuru")
    Checking.check_status_code(response=get_dostavka_guru, expected_status_code=200)
    Checking.checking_json_value(response=get_dostavka_guru, key_name="code", expected_value="DostavkaGuru")
    Checking.checking_json_value(response=get_dostavka_guru, key_name="credentials", field="visibility",
                                 expected_value=True)


@allure.description("Получения сроков доставки по СД DostavkaGuru")
def test_delivery_time_schedules(app):
    delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="DostavkaGuru")
    Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
    Checking.checking_json_value(response=delivery_time_schedules, key_name="intervals",
                                 expected_value=INFO.guru_intervals)


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД DostavkaGuru")
def test_info_vats(app):
    info_vats = app.info.info_vats(delivery_service_code="DostavkaGuru")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.guru_vats)


@allure.description("Получение актуального списка возможных сервисов заказа СД DostavkaGuru")
def test_info_statuses(app):
    info_delivery_service_services = app.info.info_delivery_service_services(code="DostavkaGuru")
    Checking.check_status_code(response=info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=info_delivery_service_services, expected_value=INFO.guru_services)


@allure.description("Создание Courier заказа по CД DostavkaGuru")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, payment_type, connections):
    day = datetime.date.today() + datetime.timedelta(days=2)
    new_order = app.order.post_order(payment_type=payment_type, type_ds="Courier", service="DostavkaGuru",
                                     declared_value=500, data=f"{day}", routes=[
                                         {
                                             "deliveryService": "RussianPost",
                                             "deferred": True
                                         }
                                     ], items_declared_value=1000, barcode=f"{randrange(1000000, 9999999)}")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=["id", "type", "url", "status"])
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Получение информации об истории изменения статусов заказа СД DostavkaGuru")
def test_order_status(app):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получения этикеток CД DostavkaGuru вне партии")
def test_get_labels_out_of_parcel(app):
    for order_id in app.order.getting_all_order_id_out_parcel():
        label = app.document.get_label(order_id=order_id, type_="termo")
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе CД DostavkaGuru")
def test_order_details(app):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии CД DostavkaGuru")
def test_create_parcel(app):
    orders_id = app.order.getting_all_order_id_out_parcel()
    create_parcel = app.parcel.post_parcel(all_orders=True, order_id=orders_id)
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение этикеток СД DostavkaGuru")
def test_get_label(app):
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    for order_id in order_in_parcel:
        label = app.document.get_label(order_id=order_id, type_="termo")
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД DostavkaGuru")
def test_get_labels_from_parcel(app):
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    labels_from_parcel = app.document.post_labels(order_ids=order_in_parcel)
    Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП СД DostavkaGuru")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД DostavkaGuru")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)
