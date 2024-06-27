from utils.checking import Checking
from utils.global_enums import INFO
from utils.environment import ENV_OBJECT
from random import choice
import pytest
import allure


@allure.description("Подключение настроек службы доставки СД FivePost по агрегации")
def test_integration_delivery_services(app, shop_id):
    five_post = app.service.post_delivery_service(shop_id=shop_id,
                                                  delivery_service=app.settings.five_post(aggregation=True))
    Checking.check_status_code(response=five_post, expected_status_code=201)
    Checking.checking_json_key(response=five_post, expected_value=INFO.created_entity)


@allure.description("Модерация СД FivePost")
def test_moderation_delivery_services(admin, shop_id):
    moderation = admin.connection.post_connections(delivery_service=admin.moderation.five_post(shop_id=shop_id))
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


@allure.description("Получение списка ПВЗ СД FivePost")
def test_delivery_service_points(app, shop_id):
    delivery_service_points = app.info.get_delivery_service_points(shop_id=shop_id, delivery_service_code="FivePost")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.check_response_is_not_empty(response=delivery_service_points)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="FivePost")


@allure.description("Получение DeliveryPoint оферов по СД FivePost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, shop_id, warehouse_id, payment_type):
    offers_delivery_point = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                                  types="DeliveryPoint", delivery_service_code="FivePost",
                                                  delivery_point_number="006bf88a-5186-45d9-9911-89d37f1edc86")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание DeliveryPoint заказа по СД FivePost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_delivery_point(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                            type_ds="DeliveryPoint", service="FivePost",
                                            delivery_point_code="006bf88a-5186-45d9-9911-89d37f1edc86",
                                            declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    order_id = new_order.json()["id"]
    connections.wait_create_order(order_id=order_id)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                               value="state"),
                                    two_value=["succeeded"])
    shared_data["order_ids"].append(order_id)


@allure.description("Создание заказа из файла СД FivePost")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, shop_id, warehouse_id, file_extension, connections):
    new_orders = app.order.post_import_order_format_metaship(shop_id=shop_id, warehouse_id=warehouse_id,
                                                             code="five_post", file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    for order in new_orders.json().values():
        connections.wait_create_order(order_id=order["id"])
        Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order["id"],
                                                                                   value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order["id"],
                                                                                   value="state"),
                                        two_value=["succeeded"])


@allure.description("Получение списка заказов CД FivePost")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД FivePost")
def test_get_order_by_id(app, shared_data):
    random_order = app.order.get_order_id(order_id=choice(shared_data["order_ids"]))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Получение информации об истории изменения статусов заказа СД FivePost")
def test_order_status(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Редактирование веса в заказе СД FivePost")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_patch_order_weight(app, shared_data):
    random_order = choice(shared_data["order_ids"])
    order_patch = app.order.patch_order_weight(order_id=random_order, weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)
    assert_order_patch = app.order.get_order_patches(order_id=order_patch.json()["id"])
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_in_list_json_value(response=assert_order_patch, key_name="state", expected_value="succeeded")


@allure.description("Редактирование информации о получателе в заказе СД FivePost")
def test_patch_order_recipient(app, shared_data):
    random_order = choice(shared_data["order_ids"])
    order_patch = app.order.patch_order_recipient(order_id=random_order, phone_number="+79266967503",
                                                  email="new_test_email@bk.ru")
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="recipient", field="phoneNumber",
                               expected_value="+79266967503")
    Checking.checking_big_json(response=order_patch, key_name="recipient", field="email",
                               expected_value="new_test_email@bk.ru")
    assert_order_patch = app.order.get_order_patches(order_id=order_patch.json()["id"])
    Checking.check_status_code(response=assert_order_patch, expected_status_code=200)
    Checking.checking_in_list_json_value(response=assert_order_patch, key_name="state", expected_value="succeeded")


@allure.description("Редактирование одноместного заказа СД FivePost")
def test_patch_single_order(app, connections, shared_data):
    random_order_id = choice(shared_data["order_ids"])
    order_patch = app.order.patch_order_items_five_post(order_id=random_order_id, items_name="семена бамбука")
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    connections.wait_create_order(order_id=random_order_id)
    order_by_id = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=order_by_id, expected_status_code=200)
    field = order_by_id.json()["data"]["request"]["places"][0]["items"][0]
    Checking.checking_json_value(response=order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=order_by_id, key_name="state", expected_value="succeeded")
    Checking.check_value_comparison(one_value=field["name"], two_value="семена бамбука")
    assert_order_patch = app.order.get_order_patches(order_id=order_patch.json()["id"])
    Checking.check_status_code(response=assert_order_patch, expected_status_code=200)
    Checking.checking_in_list_json_value(response=assert_order_patch, key_name="state", expected_value="succeeded")


@allure.description("Получение кода выдачи заказа для СД FivePost")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_generate_security_code(app, shared_data):
    random_order_id = choice(shared_data["order_ids"])
    security_code = app.order.get_generate_security_code(order_id=random_order_id)
    Checking.check_status_code(response=security_code, expected_status_code=200)
    Checking.checking_json_key(response=security_code, expected_value=["code"])


@allure.description("Удаление заказа СД FivePost")
def test_delete_order(app, connections, shared_data):
    random_order_id = shared_data["order_ids"].pop()
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=random_order_id,
                                                                               value="deleted"),
                                    two_value=[True])


@allure.description("Получения этикетки СД FivePost вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    for order_id in shared_data["order_ids"]:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД FivePost")
def test_order_details(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД FivePost")
def test_create_parcel(app, shared_data):
    random_order_id = choice(shared_data["order_ids"])
    create_parcel = app.parcel.post_parcel(value=random_order_id)
    parcel_id = create_parcel.json()[0]["id"]
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")
    shared_data["parcel_ids"].append(parcel_id)
    shared_data["order_ids_in_parcel"].append(random_order_id)
    print(shared_data["order_ids_in_parcel"])


@allure.description("Получение списка партий CД FivePost")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД FivePost")
def test_get_parcel_by_id(app, shared_data):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД FivePost (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    for order in shared_data["order_ids"]:
        random_parcel = choice(shared_data["parcel_ids"])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=random_parcel, op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        shared_data["order_ids_in_parcel"].append(order)
        print(shared_data["order_ids_in_parcel"])
        assert order in connections.get_list_all_orders_in_parcel_for_parcel_id(parcel_id=random_parcel)


@allure.description("Редактирование веса заказа в партии СД FivePost")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_patch_weight_random_order_in_parcel(app, shared_data):
    order_patch = app.order.patch_order_weight(order_id=choice(shared_data["order_ids_in_parcel"]), weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Получение этикеток СД FivePost")
def test_get_label(app, shared_data):
    for order_id in shared_data["order_ids_in_parcel"]:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД FivePost")
def test_get_labels_from_parcel(app, shared_data):
    labels_from_parcel = app.document.post_labels(parcel_id=choice(shared_data["parcel_ids"]),
                                                  order_ids=shared_data["order_ids_in_parcel"])
    Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП СД FivePost")
def test_get_app(app, shared_data):
    acceptance = app.document.get_acceptance(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД FivePost")
def test_get_documents(app, shared_data):
    documents = app.document.get_files(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание формы с этикетками партии СД FivePost")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    forms_labels = app.forms.post_forms(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=forms_labels, expected_status_code=201)
    Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)


@allure.description("Редактирование партии СД FivePost (Удаление заказа)")
def test_remove_order_in_parcel(app, connections, shared_data):
    remove_order = app.parcel.patch_parcel(op="remove", order_id=choice(shared_data["order_ids_in_parcel"]),
                                           parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=remove_order, expected_status_code=200)
    assert remove_order is not connections.get_list_all_orders_in_parcel()
