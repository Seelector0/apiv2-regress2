from utils.global_enums import INFO
from utils.checking import Checking
from random import choice, randrange
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


@allure.description("Подключение настроек СД Cdek")
def test_integration_delivery_services(app):
    cdek = app.service.post_delivery_services_cdek()
    Checking.check_status_code(response=cdek, expected_status_code=201)
    Checking.checking_json_key(response=cdek, expected_value=INFO.created_entity)


@allure.description("Получение оферов в формате 'widget'")
def test_offers_format_widget(app):
    offers_widget = app.offers.get_offers(format_="widget")
    Checking.check_status_code(response=offers_widget, expected_status_code=200)
    Checking.check_delivery_services_in_widget_offers(response=offers_widget, delivery_service="Cdek")


@allure.description("Получение Courier оферов по СД Cdek")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier", delivery_service_code="Cdek")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Получение DeliveryPoint оферов по СД Cdek")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                  delivery_service_code="Cdek")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание Courier многоместного заказа по CД Cdek")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, payment_type, connections):
    new_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="Cdek",
                                           tariff=choice(INFO.cdek_courier_tariffs), declared_value=500,
                                           barcode_1=f"{randrange(1000000, 9999999)}",
                                           barcode_2=f"{randrange(1000000, 9999999)}")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание DeliveryPoint многоместного заказа по CД Cdek")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_delivery_point(app, payment_type, connections):
    new_order = app.order.post_multi_order(payment_type=payment_type, type_ds="DeliveryPoint",
                                           service="Cdek", tariff=choice(INFO.cdek_ds_tariffs),
                                           delivery_point_code="VNG2", declared_value=500,
                                           barcode_1=f"{randrange(1000000, 9999999)}",
                                           barcode_2=f"{randrange(1000000, 9999999)}")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Добавление items в многоместный заказ СД Cdek")
def test_patch_multi_order(app, connections):
    choice_order_id = choice(connections.metaship.get_list_all_orders_out_parcel())
    old_len_order_list = app.order.get_order_id(order_id=choice_order_id)
    patch_order = app.order.patch_order_add_item(order_id=choice_order_id)
    Checking.check_status_code(response=patch_order, expected_status_code=200)
    Checking.checking_json_value(response=patch_order, key_name="status", expected_value="created")
    Checking.checking_json_value(response=patch_order, key_name="state", expected_value="editing-external-processing")
    connections.metaship.wait_create_order(order_id=choice_order_id)
    new_len_order_list = app.order.get_order_id(order_id=choice_order_id)
    Checking.check_status_code(response=new_len_order_list, expected_status_code=200)
    Checking.checking_json_value(response=new_len_order_list, key_name="status", expected_value="created")
    Checking.checking_json_value(response=new_len_order_list, key_name="state", expected_value="succeeded")
    Checking.checking_sum_len_lists(old_list=old_len_order_list.json()["data"]["request"]["places"],
                                    new_list=new_len_order_list.json()["data"]["request"]["places"])


@allure.description("Создание Courier заказа по CД Cdek")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, payment_type, connections):
    new_order = app.order.post_single_order(payment_type=payment_type, type_ds="Courier", service="Cdek",
                                            tariff=choice(INFO.cdek_courier_tariffs), declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание DeliveryPoint заказа по CД Cdek")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_delivery_point(app, payment_type, connections):
    new_order = app.order.post_single_order(payment_type=payment_type, type_ds="DeliveryPoint", service="Cdek",
                                            tariff=choice(INFO.cdek_ds_tariffs), delivery_point_code="VNG2",
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


@allure.description("Создание заказа из файла СД Cdek")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, file_extension, connections):
    new_orders = app.order.post_import_order_format_metaship(code="cdek", file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    for order in new_orders.json().values():
        connections.metaship.wait_create_order(order_id=order["id"])
        Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=order["id"],
                                                                                            value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=order["id"],
                                                                                            value="state"),
                                        two_value=["succeeded"])


@allure.description("Получение списка заказов CД Cdek")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД Cdek")
def test_get_order_by_id(app, connections):
    random_order = app.order.get_order_id(order_id=choice(connections.metaship.get_list_all_orders_out_parcel()))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Редактирование заказа СД Cdek")
def test_editing_order(app, connections):
    random_order_id = choice(connections.metaship.get_order_id_from_database(not_in_parcel=True, single_order=True))
    patch_order = app.order.patch_order(order_id=random_order_id, name="Пуфик", price=500, count=2, weight=2)
    Checking.check_status_code(response=patch_order, expected_status_code=200)
    connections.metaship.wait_create_order(order_id=random_order_id)
    order_by_id = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=order_by_id, expected_status_code=200)
    field = order_by_id.json()["data"]["request"]["places"][0]["items"][0]
    Checking.checking_json_value(response=order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=order_by_id, key_name="state", expected_value="succeeded")
    Checking.check_value_comparison(one_value=field["name"], two_value="Пуфик")
    Checking.check_value_comparison(one_value=field["price"], two_value=500)
    Checking.check_value_comparison(one_value=field["count"], two_value=2)
    Checking.check_value_comparison(one_value=field["weight"], two_value=2)


@allure.description("Редактирование веса в заказе СД Cdek")
def test_patch_order_weight(app, connections):
    random_order_id = choice(connections.metaship.get_order_id_from_database(not_in_parcel=True, single_order=True))
    order_patch = app.order.patch_order_weight(order_id=random_order_id, weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    connections.metaship.wait_create_order(order_id=random_order_id)
    get_order_by_id = app.order.get_order_id(order_id=order_patch.json()["id"])
    Checking.checking_big_json(response=get_order_by_id, key_name="weight", expected_value=4)


@allure.description("Получение информации об истории изменения статусов заказа СД Cdek")
def test_order_status(app, connections):
    for order_id in connections.metaship.get_list_all_orders_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Удаление заказа СД Cdek")
def test_delete_order(app, connections):
    random_order_id = choice(connections.metaship.get_list_all_orders_out_parcel())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=random_order_id,
                                                                                        value="deleted"),
                                    two_value=[True])


@allure.description("Получения этикеток CД Cdek вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, connections, labels):
    for order_id in connections.metaship.get_list_all_orders_out_parcel():
        label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получения оригинальных этикеток CД Cdek в формате A4, A5, A6 вне партии")
@pytest.mark.parametrize("format_", ["A4", "A5", "A6"])
def test_get_original_labels_out_of_parcel(app, connections, format_):
    for order_id in connections.metaship.get_list_all_orders_out_parcel():
        label = app.document.get_label(order_id=order_id, size_format=format_)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД Cdek")
def test_order_details(app, connections):
    for order_id in connections.metaship.get_list_all_orders_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Cdek")
def test_create_parcel(app, connections):
    create_parcel = app.parcel.post_parcel(value=choice(connections.metaship.get_list_all_orders_out_parcel()))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение списка партий CД Cdek")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД Cdek")
def test_get_parcel_by_id(app, connections):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(connections.metaship.get_list_parcels()))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД Cdek (Добавление заказов)")
def test_add_order_in_parcel(app, connections):
    list_parcel_id = connections.metaship.get_list_parcels()
    for order in connections.metaship.get_list_all_orders_out_parcel():
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=list_parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        assert order in connections.metaship.get_list_all_orders_in_parcel()


@allure.description("Редактирование веса заказа в партии СД Cdek")
def test_patch_weight_random_order_in_parcel(app, connections):
    order_in_parcel = connections.metaship.get_order_id_from_database(in_parcel=True, single_order=True)
    order_patch = app.order.patch_order_weight(order_id=choice(order_in_parcel), weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    connections.metaship.wait_create_order(order_id=order_patch.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=order_patch.json()["id"])
    Checking.checking_big_json(response=get_order_by_id, key_name="weight", expected_value=4)


@allure.description("Получение этикеток СД Cdek")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_label(app, connections, labels):
    for order_id in connections.metaship.get_list_all_orders_in_parcel():
        label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получения оригинальных этикеток CД Cdek в формате A4, A5, A6")
@pytest.mark.parametrize("format_", ["A4", "A5", "A6"])
def test_get_original_labels(app, connections, format_):
    for order_id in connections.metaship.get_list_all_orders_in_parcel():
        label = app.document.get_label(order_id=order_id, size_format=format_)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД Cdek")
def test_get_labels_from_parcel(app, connections):
    labels_from_parcel = app.document.post_labels(order_ids=connections.metaship.get_list_all_orders_in_parcel())
    Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП СД Cdek")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД Cdek")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Редактирование партии СД Cdek (Удаление заказа)")
def test_remove_order_in_parcel(app, connections):
    list_order = connections.metaship.get_list_all_orders_in_parcel()
    list_parcel_id = connections.metaship.get_list_parcels()
    remove_order = app.parcel.patch_parcel(op="remove", order_id=choice(list_order), parcel_id=list_parcel_id[0])
    Checking.check_status_code(response=remove_order, expected_status_code=200)
    assert remove_order is not connections.metaship.get_list_all_orders_in_parcel()


@allure.description("Создание забора СД Cdek")
def test_create_intake(app, connections):
    new_intake = app.intakes.post_intakes(delivery_service="Cdek")
    Checking.check_status_code(response=new_intake, expected_status_code=201)
    Checking.checking_json_key(response=new_intake, expected_value=INFO.created_entity)
    Checking.check_value_comparison(one_value=connections.metaship.get_list_intakes_value(
        intake_id=new_intake.json()["id"], value="status"), two_value=["pending"])
