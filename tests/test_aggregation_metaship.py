from utils.global_enums import INFO
from utils.checking import Checking
from random import choice
import pytest
import allure


@allure.description("Создание магазина")
@pytest.mark.parametrize("execution_number", range(2))
def test_create_shop(app, connections, execution_number):
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


@allure.description("Подключение настроек СД Boxberry по агрегации")
def test_aggregation_delivery_services_boxberry(app):
    boxberry = app.service.post_delivery_services_boxberry(aggregation=True)
    Checking.check_status_code(response=boxberry, expected_status_code=201)
    Checking.checking_json_key(response=boxberry, expected_value=INFO.created_entity)


@allure.description("Модерация СД Boxberry")
def test_moderation_delivery_services_boxberry(admin):
    moderation = admin.moderation.post_connections_boxberry()
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


@allure.description("Подключение настроек СД MetaShip по агрегации")
def test_aggregation_delivery_services_metaship(app):
    metaship = app.service.post_delivery_services_metaship()
    Checking.check_status_code(response=metaship, expected_status_code=201)
    Checking.checking_json_key(response=metaship, expected_value=INFO.created_entity)


@allure.description("Update Connection Id")
def test_update_connection_id_for_metaship(admin):
    update = admin.moderation.put_update_connection_id(settings=admin.dicts.form_settings_ds_metaship(),
                                                       index_shop_id=-1)
    Checking.check_status_code(response=update, expected_status_code=200)
    Checking.checking_json_key(response=update, expected_value=INFO.entity_connections_id)


@allure.description("Модерация СД MetaShip")
def test_moderation_delivery_services_metaship(admin):
    moderation = admin.moderation.post_connections_metaship()
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


@allure.description("Получение Courier оферов по СД MetaShip")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier", delivery_service_code="MetaShip")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Создание Courier заказа по CД MetaShip")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
@pytest.mark.parametrize("execution_number", range(2))
def test_create_order_courier(app, payment_type, connections, execution_number):
    new_order = app.order.post_single_order(payment_type=payment_type, type_ds="Courier", service="MetaShip",
                                            declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])


@allure.description("Получение списка заказов CД MetaShip")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД MetaShip")
def test_get_order_by_id(app, connections):
    random_order = app.order.get_order_id(order_id=choice(connections.get_list_all_orders_out_parcel()))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Редактирование веса в заказе СД MetaShip")
def test_patch_order_weight(app, connections):
    random_order = choice(connections.get_list_all_orders_out_parcel())
    order_patch = app.order.patch_order_weight(order_id=random_order, weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Удаление заказа CД MetaShip")
def test_delete_order(app, connections):
    random_order_id = choice(connections.get_list_all_orders_out_parcel())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=random_order_id,
                                                                               value="deleted"),
                                    two_value=[True])


@allure.description("Получения этикетки MetaShip вне партии")
def test_get_label_out_of_parcel(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение информации об истории изменения статусов заказа CД MetaShip")
def test_order_status(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе CД MetaShip")
def test_order_details(app, connections):
    for order_id in connections.get_list_all_orders_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии CД MetaShip")
def test_create_parcel(app, connections):
    create_parcel = app.parcel.post_parcel(value=connections.get_list_all_orders_out_parcel())
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение списка партий CД MetaShip")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД MetaShip")
def test_get_parcel_by_id(app, connections):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(connections.get_list_parcels()))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Получение этикетки CД MetaShip")
def test_get_labels(app, connections):
    for order_id in connections.get_list_all_orders_in_parcel():
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД MetaShip")
def test_get_labels_from_parcel(app, connections):
    labels_from_parcel = app.document.post_labels(order_ids=connections.get_list_all_orders_in_parcel())
    Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП CД MetaShip")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов CД MetaShip")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание формы с этикетками партии СД MetaShip")
def test_forms_parcels_labels(app):
    forms_labels = app.forms.post_forms()
    Checking.check_status_code(response=forms_labels, expected_status_code=201)
    Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)
