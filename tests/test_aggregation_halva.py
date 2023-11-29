from utils.global_enums import INFO
from utils.checking import Checking
from random import choice
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


@allure.description("Подключение настроек СД Halva по агрегации")
def test_aggregation_delivery_services(app):
    five_post = app.service.post_delivery_services_halva(aggregation=True)
    Checking.check_status_code(response=five_post, expected_status_code=201)
    Checking.checking_json_key(response=five_post, expected_value=INFO.created_entity)


@allure.description("Модерация СД Halva")
def test_moderation_delivery_services(admin):
    moderation = admin.moderation.post_connections_halva()
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


@allure.description("Получение списка ПВЗ СД Halva")
def test_delivery_service_points(app):
    delivery_service_points = app.info.get_delivery_service_points(delivery_service_code="Halva")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.check_response_is_not_empty(response=delivery_service_points)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="Halva")


@allure.description("Получение оферов в формате 'widget'")
def test_offers_format_widget(app):
    offers_widget = app.offers.get_offers(format_="widget")
    Checking.check_status_code(response=offers_widget, expected_status_code=200)
    Checking.check_delivery_services_in_widget_offers(response=offers_widget, delivery_service="Halva")


@allure.description("Получение DeliveryPoint оферов по СД Halva")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                  delivery_service_code="Halva")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание DeliveryPoint заказа по CД Halva")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_delivery_point(app, payment_type, connections):
    new_order = app.order.post_single_order(payment_type=payment_type, type_ds="DeliveryPoint", service="Halva",
                                            delivery_point_code="Халва-6193", declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])


@allure.description("Редактирование заказа СД Halva")
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


@allure.description("Получение списка заказов CД Halva")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД Halva")
def test_get_order_by_id(app, connections):
    random_order = app.order.get_order_id(order_id=choice(connections.get_list_all_orders_out_parcel()))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Получения этикетки Halva вне партии")
def test_get_label_out_of_parcel(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение информации об истории изменения статусов заказа CД Halva")
def test_order_status(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе CД Halva")
def test_order_details(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Halva")
def test_create_parcel(app, connections):
    create_parcel = app.parcel.post_parcel(value=choice(connections.get_list_all_orders_out_parcel()))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение списка партий CД Halva")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД Halva")
def test_get_parcel_by_id(app, connections):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(connections.get_list_parcels()))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД Halva (Добавление заказов)")
def test_add_order_in_parcel(app, connections):
    list_parcel_id = connections.get_list_parcels()
    for order in connections.get_list_all_orders_out_parcel():
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=list_parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        assert order in connections.get_list_all_orders_in_parcel()


@allure.description("Получение этикеток СД Halva")
def test_get_label(app, connections):
    for order_id in connections.get_list_all_orders_in_parcel():
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД Halva")
def test_get_labels_from_parcel(app, connections):
    labels_from_parcel = app.document.post_labels(order_ids=connections.get_list_all_orders_in_parcel())
    Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП СД Halva")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД Halva")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание формы с этикетками партии СД Halva")
def test_forms_parcels_labels(app):
    forms = app.forms.post_forms()
    Checking.check_status_code(response=forms, expected_status_code=201)


@allure.description("Редактирование партии СД Halva (Удаление заказа)")
def test_remove_order_in_parcel(app, connections):
    list_order = connections.get_list_all_orders_in_parcel()
    list_parcel_id = connections.get_list_parcels()
    remove_order = app.parcel.patch_parcel(op="remove", order_id=choice(list_order), parcel_id=list_parcel_id[0])
    Checking.check_status_code(response=remove_order, expected_status_code=200)
    assert remove_order is not connections.get_list_all_orders_in_parcel()
