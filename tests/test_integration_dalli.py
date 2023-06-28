from utils.enums.global_enums import INFO
from utils.checking import Checking
from random import choice
import datetime
import pytest
import allure


@allure.description("Создание магазина")
def test_create_integration_shop(app):
    new_shop = app.shop.post_shop()
    Checking.check_status_code(response=new_shop, expected_status_code=201)
    Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)
    get_new_shop = app.shop.get_shop_id(shop_id=new_shop.json()["id"])
    Checking.check_status_code(response=get_new_shop, expected_status_code=200)
    Checking.checking_json_value(response=get_new_shop, key_name="visibility", expected_value=True)


@allure.description("Создание склада")
def test_create_warehouse(app):
    new_warehouse = app.warehouse.post_warehouse()
    Checking.check_status_code(response=new_warehouse, expected_status_code=201)
    Checking.checking_json_key(response=new_warehouse, expected_value=INFO.created_entity)
    get_new_warehouse = app.warehouse.get_warehouse_id(warehouse_id=new_warehouse.json()["id"])
    Checking.check_status_code(response=get_new_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=get_new_warehouse, key_name="visibility", expected_value=True)


@allure.description("Подключение настроек СД Dalli")
def test_integration_delivery_services(app):
    cdek = app.service.delivery_services_dalli()
    Checking.check_status_code(response=cdek, expected_status_code=201)
    Checking.checking_json_key(response=cdek, expected_value=INFO.created_entity)
    get_dalli = app.service.get_delivery_services_code(code="Dalli")
    Checking.check_status_code(response=get_dalli, expected_status_code=200)
    Checking.checking_json_value(response=get_dalli, key_name="code", expected_value="Dalli")
    Checking.checking_json_value(response=get_dalli, key_name="credentials", field="visibility", expected_value=True)


@allure.description("Получения сроков доставки по СД Dalli")
@pytest.mark.parametrize("tariff_id", ["1", "2", "11"])
def test_delivery_time_schedules(app, tariff_id):
    delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="Dalli", tariff_id=tariff_id)
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


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД Dalli")
def test_info_vats(app):
    info_vats = app.info.info_vats(delivery_service_code="Dalli")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.dalli_vats)


@allure.description("Получение актуального списка возможных сервисов заказа СД Dalli")
def test_info_statuses(app):
    info_delivery_service_services = app.info.info_delivery_service_services(code="Dalli")
    Checking.check_status_code(response=info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=info_delivery_service_services, expected_value=INFO.dalli_services)


@allure.description("Получение оферов по СД Dalli (Courier)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier",
                                           delivery_service_code="Dalli")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Создание Courier многоместного заказа по CД Dalli")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, payment_type, connections):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    new_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="Dalli",
                                           data=str(tomorrow), tariff="1", declared_value=2000, delivery_time={
                                               "from": "18:00",
                                               "to": "22:00"
                                           }, vat="NO_VAT")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание Courier заказа по CД Dalli")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, payment_type, connections):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    new_order = app.order.post_order(payment_type=payment_type, type_ds="Courier", service="Dalli",
                                     data=str(tomorrow), tariff="1", declared_value=2000, delivery_time={
                                        "from": "18:00",
                                        "to": "22:00"
                                     }, vat="NO_VAT")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Редактирование заказа СД Dalli")
def test_editing_order(app):
    random_order = choice(app.order.getting_all_order_id_out_parcel())
    order_put = app.order.put_order(order_id=random_order, weight=5, length=12, width=14, height=11,
                                    family_name="Иванов")
    Checking.check_status_code(response=order_put, expected_status_code=200)
    Checking.checking_big_json(response=order_put, key_name="weight", expected_value=5)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="length", expected_value=12)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="width", expected_value=14)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="height", expected_value=11)
    Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName", expected_value="Иванов")


@allure.description("Получение информации об истории изменения статусов заказа СД Dalli")
def test_order_status(app):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе СД Dalli")
def test_order_details(app):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Dalli")
def test_create_parcel(app):
    orders_id = app.order.getting_all_order_id_out_parcel()
    create_parcel = app.parcel.post_parcel(order_id=choice(orders_id))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Редактирование партии СД Dalli (Добавление заказов)")
def test_add_order_in_parcel(app):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    for order in app.order.getting_all_order_id_out_parcel():
        old_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        new_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        Checking.checking_sum_len_lists(old_list=old_list_order_in_parcel, new_list=new_list_order_in_parcel)


@allure.description("Получения оригинальных этикеток CД Dalli в формате A4, A5, A6")
@pytest.mark.parametrize("format_", ["A4", "A5", "A6"])
def test_get_original_labels(app, format_):
    order_in_parcel = app.order.getting_all_order_in_parcel()
    for order_id in order_in_parcel:
        label = app.document.get_label(order_id=order_id, size_format=format_)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикетки СД Dalli")
def test_get_label(app):
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    for order_id in order_in_parcel:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД Dalli")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД Dalli")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)
