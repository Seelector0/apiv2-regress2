from utils.checking import Checking
from utils.enums.global_enums import INFO
from random import choice
import pytest
import allure


@allure.description("Создание магазина")
def test_create_integration_shop(app, token):
    new_shop = app.shop.post_shop()
    Checking.check_status_code(response=new_shop, expected_status_code=201)
    Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)
    get_new_shop = app.shop.get_shop_id(shop_id=new_shop.json()["id"])
    Checking.check_status_code(response=get_new_shop, expected_status_code=200)
    Checking.checking_json_value(response=get_new_shop, key_name="visibility", expected_value=True)


@allure.description("Создание склада")
def test_create_warehouse(app, token):
    new_warehouse = app.warehouse.post_warehouse()
    Checking.check_status_code(response=new_warehouse, expected_status_code=201)
    Checking.checking_json_key(response=new_warehouse, expected_value=INFO.created_entity)
    get_new_warehouse = app.warehouse.get_warehouse_id(warehouse_id=new_warehouse.json()["id"])
    Checking.check_status_code(response=get_new_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=get_new_warehouse, key_name="visibility", expected_value=True)


@allure.description("Подключение настроек службы доставки СД FivePost")
def test_integration_delivery_services(app, token):
    five_post = app.service.delivery_services_five_post()
    Checking.check_status_code(response=five_post, expected_status_code=201)
    Checking.checking_json_key(response=five_post, expected_value=INFO.created_entity)
    get_five_post = app.service.get_delivery_services_code(code="FivePost")
    Checking.check_status_code(response=get_five_post, expected_status_code=200)
    Checking.checking_json_value(response=get_five_post, key_name="code", expected_value="FivePost")
    Checking.checking_json_value(response=get_five_post, key_name="credentials", field="visibility",
                                 expected_value=True)


@allure.description("Получение списка ПВЗ СД FivePost")
def test_delivery_service_points(app, token):
    delivery_service_points = app.info.delivery_service_points(delivery_service_code="FivePost")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="FivePost")


@allure.description("Получения сроков доставки по СД FivePost")
def test_delivery_time_schedules(app, token):
    delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="FivePost")
    Checking.check_status_code(response=delivery_time_schedules, expected_status_code=400)


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД FivePost")
def test_info_vats(app, token):
    info_vats = app.info.info_vats(delivery_service_code="FivePost")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.FIVE_POST_VATS)


@allure.description("Получение оферов по СД FivePost (DeliveryPoint)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type, token):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                  delivery_service_code="FivePost",
                                                  delivery_point_number="0014e8fe-1c2d-4429-b115-c9064ce54c30")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание DeliveryPoint заказа по СД FivePost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_delivery_point(app, payment_type, token):
    new_order = app.order.post_order(payment_type=payment_type, type_ds="DeliveryPoint", service="FivePost",
                                     delivery_point_code="0014e8fe-1c2d-4429-b115-c9064ce54c30", price=1000,
                                     declared_value=1500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"], sec=5)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание заказа из файла СД FivePost")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, token, file_extension):
    new_orders = app.order.post_import_order(delivery_services="five_post", file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    app.time_sleep(sec=5)
    for order in new_orders.json().values():
        get_order_by_id = app.order.get_order_id(order_id=order["id"])
        Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
        Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Получение информации об истории изменения статусов заказа СД FivePost")
def test_order_status(app, token):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Редактирование веса в заказе СД FivePost")
@pytest.mark.skip("Не редактируется вес заказа нужен МОК")
def test_patch_order_weight(app, token):
    random_order = choice(app.order.getting_all_order_id_out_parcel())
    order_patch = app.order.patch_order(order_id=random_order, path="weight", weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Удаление заказа СД FivePost")
def test_delete_order(app, token):
    random_order_id = choice(app.order.getting_all_order_id_out_parcel())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    get_order_by_id = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=404)


@allure.description("Попытка получения этикетки СД FivePost вне партии")
def test_get_label_of_parcel(app, token):
    for order_id in app.order.getting_all_order_id_out_parcel():
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД FivePost")
def test_order_details(app, token):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД FivePost")
def test_create_parcel(app, token):
    orders_id = app.order.getting_all_order_id_out_parcel()
    create_parcel = app.parcel.post_parcel(order_id=choice(orders_id))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Редактирование веса заказа в партии СД FivePost")
@pytest.mark.skip("Не редактируется вес заказа нужен МОК")
def test_patch_weight_random_order_in_parcel(app, token):
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    order_patch = app.order.patch_order(order_id=choice(order_in_parcel), path="weight", weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Редактирование партии СД FivePost (Добавление заказов)")
def test_add_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    for order in app.order.getting_all_order_id_out_parcel():
        old_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        new_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        Checking.checking_sum_len_lists(old_list=old_list_order_in_parcel, new_list=new_list_order_in_parcel)


@allure.description("Получение этикеток СД FivePost")
def test_get_label(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    for order_id in app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0]):
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД FivePost")
def test_get_labels_from_parcel(app):
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    labels_from_parcel = app.document.post_labels(order_ids=order_in_parcel)
    Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП СД FivePost")
def test_get_app(app, token):
    app = app.document.get_acceptance()
    Checking.check_status_code(response=app, expected_status_code=200)


@allure.description("Получение документов СД FivePost")
def test_get_documents(app, token):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Редактирование партииСД FivePost (Удаление заказа)")
def test_remove_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    old_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    parcel_remove = app.parcel.patch_parcel(order_id=choice(order_in_parcel), parcel_id=parcel_id[0], op="remove")
    new_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    Checking.check_status_code(response=parcel_remove, expected_status_code=200)
    Checking.checking_difference_len_lists(old_list=old_list_order, new_list=new_list_order)
