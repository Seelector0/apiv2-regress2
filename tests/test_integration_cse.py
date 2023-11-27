from utils.global_enums import INFO
from utils.checking import Checking
from random import choice
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


@allure.description("Подключение настроек службы доставки СД Cse")
def test_integration_delivery_services(app):
    cse = app.service.post_delivery_services_cse()
    Checking.check_status_code(response=cse, expected_status_code=201)
    Checking.checking_json_key(response=cse, expected_value=INFO.created_entity)


@allure.description("Получение списка ПВЗ СД Cse")
def test_delivery_service_points(app):
    delivery_service_points = app.info.get_delivery_service_points(delivery_service_code="Cse")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.check_response_is_not_empty(response=delivery_service_points)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="Cse")


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.xfail
def test_offers_format_widget(app):
    offers_widget = app.offers.get_offers(format_="widget")
    Checking.check_status_code(response=offers_widget, expected_status_code=200)
    Checking.check_delivery_services_in_widget_offers(response=offers_widget, delivery_service="Cse")


@allure.description("Получение оферов Courier по СД Cse")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier", delivery_service_code="Cse")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Создание Courier многоместного заказа по CД Cse")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, payment_type, connections):
    new_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="Cse",
                                           tariff="64", declared_value=1500, dimension=app.dicts.dimension(),
                                           date_pickup=f"{datetime.date.today()}")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание DeliveryPoint многоместного заказа по CД Cse")
def test_create_multi_order_delivery_point(app, connections):
    new_order = app.order.post_multi_order(payment_type="Paid", type_ds="DeliveryPoint", service="Cse",
                                           tariff="64", date_pickup=f"{datetime.date.today()}",
                                           dimension=app.dicts.dimension(),
                                           delivery_point_code="0299ca01-ed73-11e8-80c9-7cd30aebf951",
                                           declared_value=1500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание Courier заказа по СД Cse")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, payment_type, connections):
    new_order = app.order.post_single_order(payment_type=payment_type, type_ds="Courier", service="Cse", tariff="64",
                                            date_pickup=f"{datetime.date.today()}", declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание DeliveryPoint заказа по CД Cse")
def test_create_order_delivery_point(app, connections):
    new_order = app.order.post_single_order(payment_type="Paid", type_ds="DeliveryPoint", service="Cse", tariff="64",
                                            date_pickup=f"{datetime.date.today()}", declared_value=500,
                                            delivery_point_code="0299ca01-ed73-11e8-80c9-7cd30aebf951")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])


@allure.description("Получение списка заказов CД Cse")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД Cse")
def test_get_order_by_id(app, connections):
    random_order = app.order.get_order_id(order_id=choice(connections.get_list_all_orders_out_parcel()))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Получение информации об истории изменения статусов заказа СД Cse")
def test_order_status(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Удаление заказа СД Cse")
def test_delete_order(app, connections):
    random_order_id = choice(connections.get_list_all_orders_out_parcel())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=random_order_id,
                                                                               value="deleted"),
                                    two_value=[True])


@allure.description("Получения этикеток CД Cse вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, connections, labels):
    for order_id in connections.get_list_all_orders_out_parcel():
        label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД Cse")
def test_order_details(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Cse")
def test_create_parcel(app, connections):
    create_parcel = app.parcel.post_parcel(value=choice(connections.get_list_all_orders_out_parcel()))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение списка партий CД Cse")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД Cse")
def test_get_parcel_by_id(app, connections):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(connections.get_list_parcels()))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД Cse (Добавление заказов)")
def test_add_order_in_parcel(app, connections):
    list_parcel_id = connections.get_list_parcels()
    for order in connections.get_list_all_orders_out_parcel():
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=list_parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        assert order in connections.get_list_all_orders_in_parcel()


@allure.description("Получение этикеток СД Cse")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_label(app, connections, labels):
    for order_id in connections.get_list_all_orders_in_parcel():
        label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД Cse")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД Cse")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Редактирование партии СД Cse (Удаление заказа)")
def test_remove_order_in_parcel(app, connections):
    list_order = connections.get_list_all_orders_in_parcel()
    list_parcel_id = connections.get_list_parcels()
    remove_order = app.parcel.patch_parcel(op="remove", order_id=choice(list_order), parcel_id=list_parcel_id[0])
    Checking.check_status_code(response=remove_order, expected_status_code=200)
    assert remove_order is not connections.get_list_all_orders_in_parcel()


@allure.description("Создание забора СД Cse")
def test_create_intake(app, connections):
    new_intake = app.intakes.post_intakes(delivery_service="Cse")
    Checking.check_status_code(response=new_intake, expected_status_code=201)
    Checking.checking_json_key(response=new_intake, expected_value=INFO.created_entity)
    get_new_intake = app.intakes.get_intakes_id(intakes_id=new_intake.json()["id"])
    Checking.check_status_code(response=get_new_intake, expected_status_code=200)
    Checking.check_value_comparison(one_value=connections.get_list_intakes_value(
        intake_id=new_intake.json()["id"], value="status"), two_value=["created"])
