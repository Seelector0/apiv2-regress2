from utils.global_enums import INFO
from utils.checking import Checking
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


@allure.description("Подключение настроек СД RussianPost по агрегации")
def test_aggregation_delivery_services(app):
    russian_post = app.service.delivery_services_russian_post(aggregation=True)
    Checking.check_status_code(response=russian_post, expected_status_code=201)
    Checking.checking_json_key(response=russian_post, expected_value=INFO.created_entity)


@allure.description("Модерация СД RussianPost")
def test_moderation_delivery_services(admin):
    moderation = admin.moderation.moderation_russian_post()
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


@allure.description("Получение списка ПВЗ СД RussianPost")
def test_delivery_service_points(app):
    delivery_service_points = app.info.delivery_service_points(delivery_service_code="RussianPost")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.check_response_is_not_empty(response=delivery_service_points)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="RussianPost")


@allure.description("Получения сроков доставки по СД RussianPost")
def test_delivery_time_schedules(app):
    delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="RussianPost")
    Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
    Checking.checking_json_key(response=delivery_time_schedules, expected_value=["schedule", "intervals"])


@allure.description("Получение Courier оферов по СД RussianPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier",
                                           delivery_service_code="RussianPost")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Получение DeliveryPoint оферов по СД RussianPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                  delivery_service_code="RussianPost")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["PostOffice"])


@allure.description("Получение PostOffice оферов по СД RussianPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_russian_post(app, payment_type):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="PostOffice",
                                                  delivery_service_code="RussianPost")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["PostOffice"])


@allure.description("Создание Courier заказа по СД RussianPost")
def test_create_order_courier(app, connections):
    new_order = app.order.post_single_order(payment_type="Paid", type_ds="Courier", service="RussianPost",
                                            tariff=choice(INFO.rp_courier_tariffs), declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание DeliveryPoint заказа по СД RussianPost")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "connections", reason="Не работает на dev стенде")
def test_create_delivery_point(app, connections):
    new_order = app.order.post_single_order(payment_type="Paid", length=15, width=15, height=15,
                                            type_ds="DeliveryPoint", service="RussianPost",
                                            tariff=INFO.rp_po_tariffs[0], delivery_point_code="914841",
                                            declared_value=1000)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание PostOffice заказа по СД RussianPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_post_office(app, payment_type, connections):
    new_order = app.order.post_single_order(payment_type=payment_type, type_ds="PostOffice", service="RussianPost",
                                            tariff=choice(INFO.rp_po_tariffs), declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Редактирование заказа СД RussianPost")
def test_editing_order(app, connections):
    random_order = choice(connections.metaship.get_list_all_orders())
    order_put = app.order.put_order(order_id=random_order, weight=5, length=12, width=14, height=11,
                                    family_name="Иванов")
    Checking.check_status_code(response=order_put, expected_status_code=200)
    Checking.checking_big_json(response=order_put, key_name="weight", expected_value=5)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="length", expected_value=12)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="width", expected_value=14)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="height", expected_value=11)
    Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName", expected_value="Иванов")


@allure.description("Редактирование веса в заказе СД RussianPost")
def test_patch_order_weight(app, connections):
    random_order = choice(connections.metaship.get_list_all_orders())
    order_patch = app.order.patch_order_weight(order_id=random_order, weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Создание заказа из файла")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, file_extension, connections):
    new_orders = app.order.post_import_order_format_metaship(code="russian_post", file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    for order in new_orders.json().values():
        connections.metaship.wait_create_order(order_id=order["id"])
        Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=order["id"],
                                                                                            value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=order["id"],
                                                                                            value="state"),
                                        two_value=["succeeded"])


@allure.description("Создание заказа из файла формата СД RussianPost")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file_format_russian_post(app, file_extension, connections):
    new_orders = app.order.post_import_order_format_russian_post(file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    for order in new_orders.json().values():
        connections.metaship.wait_create_order(order_id=order["id"])
        Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=order["id"],
                                                                                            value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=order["id"],
                                                                                            value="state"),
                                        two_value=["succeeded"])


@allure.description("Получение списка заказов CД RussianPost")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД RussianPost")
def test_get_order_by_id(app, connections):
    random_order = app.order.get_order_id(order_id=choice(connections.metaship.get_list_all_orders()))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Удаление заказа СД RussianPost")
def test_delete_order(app, connections):
    random_order_id = choice(connections.metaship.get_list_all_orders())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=random_order_id,
                                                                                        value="deleted"),
                                    two_value=[True])


@allure.description("Получение информации об истории изменения статусов заказа СД RussianPost")
def test_order_status(app, connections):
    for order_id in connections.metaship.get_list_all_orders():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе СД RussianPost")
def test_order_details(app, connections):
    for order_id in connections.metaship.get_list_all_orders():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД RussianPost")
def test_create_parcel(app, connections):
    create_parcel = app.parcel.post_parcel(value=choice(connections.metaship.get_list_all_orders()))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение списка партий CД RussianPost")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД RussianPost")
def test_get_parcel_by_id(app, connections):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(connections.metaship.get_list_parcels()))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД RussianPost (Добавление заказов)")
def test_add_order_in_parcel(app, connections):
    list_parcel_id = connections.metaship.get_list_parcels()
    for order in connections.metaship.get_list_all_orders():
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=list_parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=list_parcel_id[0])
        assert order in list_order_in_parcel


@allure.description("Редактирование партии СД RussianPost (Изменение даты отправки партии)")
def test_change_shipment_date(app, connections):
    parcel_id = connections.metaship.get_list_parcels()
    shipment_date = app.parcel.patch_parcel_shipment_date(parcel_id=parcel_id[0], day=5)
    Checking.check_status_code(response=shipment_date, expected_status_code=200)
    new_date = shipment_date.json()["data"]["request"]["shipmentDate"]
    Checking.check_date_change(calendar_date=new_date, number_of_days=5)


@allure.description("Получение этикетки СД RussianPost")
def test_get_label(app, connections):
    for order_id in connections.metaship.get_list_all_orders_in_parcel():
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД RussianPost")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД RussianPost")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Редактирование партии СД RussianPost (Удаление заказа из партии)")
def test_remove_order_in_parcel(app, connections):
    parcel_id = connections.metaship.get_list_parcels()
    old_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    parcel_remove = app.parcel.patch_parcel(order_id=choice(old_list_order), parcel_id=parcel_id[0], op="remove")
    new_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    Checking.check_status_code(response=parcel_remove, expected_status_code=200)
    Checking.checking_difference_len_lists(old_list=old_list_order, new_list=new_list_order)
