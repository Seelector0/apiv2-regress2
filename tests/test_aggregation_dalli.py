from utils.global_enums import INFO
from utils.checking import Checking
from random import choice, randrange
import datetime
import pytest
import allure


@allure.description("Создание магазина")
def test_create_shop(app, connections):
    if len(connections.get_list_shops()) == 0:
        new_shop = app.shop.post_shop()
        Checking.check_status_code(response=new_shop, expected_status_code=201)
        Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)
        Checking.check_value_comparison(
            one_value=connections.get_list_shops_value(shop_id=new_shop.json()["id"], value="deleted"),
            two_value=[False])
        Checking.check_value_comparison(
            one_value=connections.get_list_shops_value(shop_id=new_shop.json()["id"], value="visibility"),
            two_value=[True])


@allure.description("Создание склада")
def test_create_warehouse(app, connections):
    if len(connections.get_list_warehouses()) == 0:
        new_warehouse = app.warehouse.post_warehouse()
        Checking.check_status_code(response=new_warehouse, expected_status_code=201)
        Checking.checking_json_key(response=new_warehouse, expected_value=INFO.created_entity)
        Checking.check_value_comparison(
            one_value=connections.get_list_warehouses_value(warehouse_id=new_warehouse.json()["id"], value="deleted"),
            two_value=[False])
        Checking.check_value_comparison(
            one_value=connections.get_list_warehouses_value(warehouse_id=new_warehouse.json()["id"],
                                                            value="visibility"),
            two_value=[True])


@allure.description("Подключение настроек СД Dalli по агрегации")
def test_aggregation_delivery_services(app):
    dalli = app.service.post_delivery_services_dalli(aggregation=True)
    Checking.check_status_code(response=dalli, expected_status_code=201)
    Checking.checking_json_key(response=dalli, expected_value=INFO.created_entity)


@allure.description("Модерация СД Dalli")
def test_moderation_delivery_services(admin):
    moderation = admin.moderation.post_connections_dalli()
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


@allure.description("Получения сроков доставки по СД Dalli")
@pytest.mark.parametrize("tariff_id", ["1", "2", "11"])
def test_delivery_time_schedules(app, tariff_id):
    delivery_time_schedules = app.info.get_delivery_time_schedules(delivery_service_code="Dalli", tariff_id=tariff_id)
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
def test_offers_courier(app, payment_type):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier",
                                           delivery_service_code="Dalli")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Создание Courier многоместного заказа по CД Dalli")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, payment_type, connections):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    if payment_type == "PayOnDelivery":
        new_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="Dalli",
                                               data=str(tomorrow), tariff="1", declared_value=0, delivery_time={
                                                   "from": "18:00",
                                                   "to": "22:00"
                                               }, barcode_1=f"{randrange(1000000, 9999999)}",
                                               barcode_2=f"{randrange(1000000, 9999999)}", cod=2100.24)
    else:
        new_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="Dalli",
                                               data=str(tomorrow), tariff="1", declared_value=0, delivery_time={
                                                   "from": "18:00",
                                                   "to": "22:00"
                                               }, barcode_1=f"{randrange(1000000, 9999999)}",
                                               barcode_2=f"{randrange(1000000, 9999999)}")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание Courier заказа по CД Dalli")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, payment_type, connections):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    if payment_type == "PayOnDelivery":
        new_order = app.order.post_single_order(payment_type=payment_type, type_ds="Courier", service="Dalli",
                                                cod=3100.24, data=str(tomorrow), tariff="1", declared_value=0,
                                                delivery_time={
                                                    "from": "18:00",
                                                    "to": "22:00"
                                                })
    else:
        new_order = app.order.post_single_order(payment_type=payment_type, type_ds="Courier", service="Dalli",
                                                data=str(tomorrow), tariff="1", declared_value=3000, delivery_time={
                                                    "from": "18:00",
                                                    "to": "22:00"
                                                })
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])


@allure.description("Получение списка заказов CД Dalli")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД Dalli")
def test_get_order_by_id(app, connections):
    random_order = app.order.get_order_id(order_id=choice(connections.get_list_all_orders_out_parcel()))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Редактирование заказа СД Dalli")
def test_editing_order(app, connections):
    random_order = choice(connections.get_list_all_orders_out_parcel())
    order_put = app.order.put_order(order_id=random_order, weight=5, length=12, width=14, height=11,
                                    family_name="Иванов")
    Checking.check_status_code(response=order_put, expected_status_code=200)
    Checking.checking_big_json(response=order_put, key_name="weight", expected_value=5)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="length", expected_value=12)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="width", expected_value=14)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="height", expected_value=11)
    Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName", expected_value="Иванов")


@allure.description("Получение информации об истории изменения статусов заказа СД Dalli")
def test_order_status(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получения этикеток CД Dalli вне партии")
def test_get_labels_out_of_parcel(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД Dalli")
def test_order_details(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Dalli")
def test_create_parcel(app, connections):
    create_parcel = app.parcel.post_parcel(value=choice(connections.get_list_all_orders_out_parcel()))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение списка партий CД Dalli")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД Dalli")
def test_get_parcel_by_id(app, connections):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(connections.get_list_parcels()))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД Dalli (Добавление заказов)")
def test_add_order_in_parcel(app, connections):
    list_parcel_id = connections.get_list_parcels()
    for order in connections.get_list_all_orders_out_parcel():
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=list_parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        assert order in connections.get_list_all_orders_in_parcel()


@allure.description("Получение этикеток СД Dalli")
def test_get_label(app, connections):
    for order_id in connections.get_list_all_orders_in_parcel():
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


@allure.description("Создание формы с этикетками партии СД Dalli")
def test_forms_parcels_labels(app):
    forms_labels = app.forms.post_forms()
    Checking.check_status_code(response=forms_labels, expected_status_code=201)
    Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)
