from utils.checking import Checking
from utils.global_enums import INFO
from environment import ENV_OBJECT
from random import choice
import pytest
import allure


@allure.description("Создание магазина")
def test_create_shop(app, connections):
    new_shop = app.shop.post_shop()
    Checking.check_status_code(response=new_shop, expected_status_code=201)
    Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_shops_value(shop_id=new_shop.json()["id"], value="deleted"),
        two_value=[False])
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_shops_value(shop_id=new_shop.json()["id"], value="visibility"),
        two_value=[True])


@allure.description("Создание склада")
def test_create_warehouse(app, connections):
    new_warehouse = app.warehouse.post_warehouse()
    Checking.check_status_code(response=new_warehouse, expected_status_code=201)
    Checking.checking_json_key(response=new_warehouse, expected_value=INFO.created_entity)
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_warehouses_value(warehouse_id=new_warehouse.json()["id"],
                                                                 value="deleted"),
        two_value=[False])
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_warehouses_value(warehouse_id=new_warehouse.json()["id"],
                                                                 value="visibility"),
        two_value=[True])


@allure.description("Подключение настроек СД FivePost по агрегации")
def test_aggregation_delivery_services(app):
    five_post = app.service.delivery_services_five_post(aggregation=True)
    Checking.check_status_code(response=five_post, expected_status_code=201)
    Checking.checking_json_key(response=five_post, expected_value=INFO.created_entity)


@allure.description("Модерация СД FivePost")
def test_moderation_delivery_services(admin):
    moderation = admin.moderation.moderation_five_post()
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


@allure.description("Получение списка ПВЗ СД FivePost")
def test_delivery_service_points(app):
    delivery_service_points = app.info.delivery_service_points(delivery_service_code="FivePost")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="FivePost")


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД FivePost")
def test_info_vats(app):
    info_vats = app.info.info_vats(delivery_service_code="FivePost")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.FIVE_POST_VATS)


@allure.description("Получение DeliveryPoint оферов по СД FivePost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                  delivery_service_code="FivePost",
                                                  delivery_point_number="006bf88a-5186-45d9-9911-89d37f1edc86")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание DeliveryPoint заказа по СД FivePost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_delivery_point(app, payment_type, connections):
    new_order = app.order.post_single_order(payment_type=payment_type, type_ds="DeliveryPoint", service="FivePost",
                                            delivery_point_code="006bf88a-5186-45d9-9911-89d37f1edc86",
                                            declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание заказа из файла СД FivePost")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, file_extension, connections):
    new_orders = app.order.post_import_order_format_metaship(code="five_post", file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    for order in new_orders.json().values():
        connections.metaship.wait_create_order(order_id=order["id"])
        Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=order["id"],
                                                                                            value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=order["id"],
                                                                                            value="state"),
                                        two_value=["succeeded"])


@allure.description("Получение информации об истории изменения статусов заказа СД FivePost")
def test_order_status(app, connections):
    for order_id in connections.metaship.get_list_all_orders():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Редактирование веса в заказе СД FivePost")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
def test_patch_order_weight(app, connections):
    random_order = choice(connections.metaship.get_list_all_orders())
    order_patch = app.order.patch_order_weight(order_id=random_order, weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Удаление заказа СД FivePost")
def test_delete_order(app, connections):
    random_order_id = choice(connections.metaship.get_list_all_orders())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=random_order_id,
                                                                                        value="deleted"),
                                    two_value=[True])


@allure.description("Получения этикетки СД FivePost вне партии")
def test_get_labels_out_of_parcel(app, connections):
    for order_id in connections.metaship.get_list_all_orders():
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД FivePost")
def test_order_details(app, connections):
    for order_id in connections.metaship.get_list_all_orders():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД FivePost")
def test_create_parcel(app, connections):
    create_parcel = app.parcel.post_parcel(value=choice(connections.metaship.get_list_all_orders()))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Редактирование партии СД FivePost (Добавление заказов)")
def test_add_order_in_parcel(app, connections):
    list_parcel_id = connections.metaship.get_list_parcels()
    for order in connections.metaship.get_list_all_orders():
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=list_parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=list_parcel_id[0])
        assert order in list_order_in_parcel


@allure.description("Редактирование веса заказа в партии СД FivePost")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
def test_patch_weight_random_order_in_parcel(app, connections):
    order_in_parcel = connections.metaship.get_list_all_orders_in_parcel()
    order_patch = app.order.patch_order_weight(order_id=choice(order_in_parcel), weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Получение этикеток СД FivePost")
def test_get_label(app, connections):
    for order_id in connections.metaship.get_list_all_orders_in_parcel():
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД FivePost")
def test_get_labels_from_parcel(app, connections):
    order_in_parcel = connections.metaship.get_list_all_orders_in_parcel()
    labels_from_parcel = app.document.post_labels(order_ids=order_in_parcel)
    Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП СД FivePost")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД FivePost")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Редактирование партииСД FivePost (Удаление заказа)")
def test_remove_order_in_parcel(app, connections):
    parcel_id = connections.metaship.get_list_parcels()
    old_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    parcel_remove = app.parcel.patch_parcel(order_id=choice(old_list_order), parcel_id=parcel_id[0], op="remove")
    new_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    Checking.check_status_code(response=parcel_remove, expected_status_code=200)
    Checking.checking_difference_len_lists(old_list=old_list_order, new_list=new_list_order)
