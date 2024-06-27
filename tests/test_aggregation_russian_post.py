from utils.global_enums import INFO
from utils.checking import Checking
from utils.environment import ENV_OBJECT
from random import choice
import pytest
import allure


@allure.description("Подключение настроек СД RussianPost по агрегации")
def test_aggregation_delivery_services(app, shop_id):
    russian_post = app.service.post_delivery_service(shop_id=shop_id,
                                                     delivery_service=app.settings.russian_post(aggregation=True))
    Checking.check_status_code(response=russian_post, expected_status_code=201)
    Checking.checking_json_key(response=russian_post, expected_value=INFO.created_entity)


@allure.description("Модерация СД RussianPost")
def test_moderation_delivery_services(admin, shop_id):
    moderation = admin.connection.post_connections(delivery_service=admin.moderation.russian_post(shop_id=shop_id))
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


@allure.description("Получение списка ПВЗ СД RussianPost")
def test_delivery_service_points(app, shop_id):
    delivery_service_points = app.info.get_delivery_service_points(shop_id=shop_id, delivery_service_code="RussianPost")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.check_response_is_not_empty(response=delivery_service_points)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="RussianPost")


@allure.description("Получение Courier оферов по СД RussianPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, shop_id, warehouse_id, payment_type):
    offers_courier = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                           types="Courier", delivery_service_code="RussianPost")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Получение DeliveryPoint оферов по СД RussianPost")
def test_offers_delivery_point(app, shop_id, warehouse_id):
    offers_delivery_point = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                                  types="DeliveryPoint", delivery_service_code="RussianPost")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Получение PostOffice оферов по СД RussianPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_post_office(app, shop_id, warehouse_id, payment_type):
    offers_delivery_point = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                                  types="PostOffice", delivery_service_code="RussianPost")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["PostOffice"])


@allure.description("Создание Courier заказа по СД RussianPost")
def test_create_order_courier(app, shop_id, warehouse_id, connections, shared_data):
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                            type_ds="Courier", service="RussianPost",
                                            tariff=choice(INFO.rp_courier_tariffs), declared_value=500)
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
    shared_data["orders_courier"].append(order_id)


@allure.description("Создание DeliveryPoint(terminal) заказа по СД RussianPost")
# @pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "connections", reason="Не работает на dev стенде")
def test_create_delivery_point_terminal(app, shop_id, warehouse_id, connections, shared_data):
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                            length=15, width=15, height=15, type_ds="DeliveryPoint",
                                            service="RussianPost", tariff=INFO.rp_po_tariffs[0],
                                            delivery_point_code="914841", declared_value=1000)
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
    shared_data["orders_terminal"].append(order_id)


@allure.description("Создание DeliveryPoint заказа по СД RussianPost")
# @pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "connections", reason="Не работает на dev стенде")
def test_create_delivery_point(app, shop_id, warehouse_id, connections, shared_data):
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type="Paid",
                                            length=15, width=15, height=15, type_ds="DeliveryPoint",
                                            service="RussianPost", tariff=INFO.rp_dp_tariffs[0],
                                            delivery_point_code="980254", declared_value=1000)
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
    shared_data["orders_delivery_point"].append(order_id)


@allure.description("Создание PostOffice заказа по СД RussianPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_post_office(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                            type_ds="PostOffice", service="RussianPost",
                                            tariff=choice(INFO.rp_po_tariffs), declared_value=500)
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
    shared_data["orders_post_office"].append(order_id)


@allure.description("Редактирование заказа СД RussianPost")
def test_editing_order(app, shared_data):
    random_order = choice(shared_data["order_ids"])
    order_put = app.order.put_order(order_id=random_order, delivery_service="RussianPost", weight=5, length=12,
                                    width=14, height=11, family_name="Иванов", first_name="Петр",
                                    second_name="Сергеевич", phone_number="+79097859012", email="new_test@mail.ru",
                                    address="119634 ул. Лукинская, дом 1, кв. 1", comment="Всё зашибись.")
    Checking.check_status_code(response=order_put, expected_status_code=200)
    Checking.checking_big_json(response=order_put, key_name="weight", expected_value=5)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="length", expected_value=12)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="width", expected_value=14)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="height", expected_value=11)
    Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName", expected_value="Иванов")
    Checking.checking_big_json(response=order_put, key_name="recipient", field="firstName", expected_value="Петр")
    Checking.checking_big_json(response=order_put, key_name="recipient", field="secondName", expected_value="Сергеевич")
    Checking.checking_big_json(response=order_put, key_name="recipient", field="phoneNumber",
                               expected_value="+79097859012")
    Checking.checking_big_json(response=order_put, key_name="recipient", field="email",
                               expected_value="new_test@mail.ru")
    Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName", expected_value="Иванов")
    Checking.checking_big_json(response=order_put, key_name="recipient", field="address",
                               expected_value={
                                   "raw": "119634 ул. Лукинская, дом 1, кв. 1",
                                   "countryCode": None
                               })


@allure.description("Редактирование веса в заказе СД RussianPost")
def test_patch_order_weight(app, shared_data):
    random_order = choice(shared_data["order_ids"])
    order_patch = app.order.patch_order_weight(order_id=random_order, weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Создание заказа из файла")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, shop_id, warehouse_id, file_extension, connections, shared_data):
    new_orders = app.order.post_import_order_format_metaship(shop_id=shop_id, warehouse_id=warehouse_id,
                                                             code="russian_post", file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    for order in new_orders.json().values():
        connections.wait_create_order(order_id=order["id"])
        Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order["id"],
                                                                                   value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order["id"],
                                                                                   value="state"),
                                        two_value=["succeeded"])


@allure.description("Создание заказа из файла формата СД RussianPost")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file_format_russian_post(app, shop_id, warehouse_id, file_extension, connections,
                                                    shared_data):
    new_orders = app.order.post_import_order_format_russian_post(shop_id=shop_id, warehouse_id=warehouse_id,
                                                                 file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    for order in new_orders.json().values():
        connections.wait_create_order(order_id=order["id"])
        Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order["id"],
                                                                                   value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=order["id"],
                                                                                   value="state"),
                                        two_value=["succeeded"])


@allure.description("Удаление заказа СД RussianPost")
def test_delete_order(app, connections, shared_data):
    random_order_id = shared_data["order_ids"].pop()
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.get_list_order_value(order_id=random_order_id,
                                                                               value="deleted"),
                                    two_value=[True])
    lists_to_check = ["orders_courier", "orders_delivery_point", "orders_post_office", "orders_terminal"]
    for list_name in lists_to_check:
        if random_order_id in shared_data[list_name]:
            shared_data[list_name].remove(random_order_id)


@allure.description("Получение списка заказов CД RussianPost")
def test_get_orders(app):
    list_orders = app.order.get_orders()
    Checking.check_status_code(response=list_orders, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_orders)


@allure.description("Получение информации о заказе CД RussianPost")
def test_get_order_by_id(app, shared_data):
    random_order = app.order.get_order_id(order_id=choice(shared_data["order_ids"]))
    Checking.check_status_code(response=random_order, expected_status_code=200)
    Checking.checking_json_key(response=random_order, expected_value=INFO.entity_order)


@allure.description("Получение информации об истории изменения статусов заказа СД RussianPost")
def test_order_status(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе СД RussianPost")
def test_order_details(app, shared_data):
    for order_id in shared_data["order_ids"]:
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД RussianPost")
@pytest.mark.parametrize("types", ["orders_courier", "orders_delivery_point", "orders_post_office", "orders_terminal"])
def test_create_parcel(app, shared_data, types):
    order = shared_data[types].pop()
    create_parcel = app.parcel.post_parcel(value=order)
    parcel_id = create_parcel.json()[0]["id"]
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")
    shared_data["parcel_ids"].append(parcel_id)
    shared_data["order_ids_in_parcel"].append(order)


@allure.description("Получение списка партий CД RussianPost")
def test_get_parcels(app):
    list_parcel = app.parcel.get_parcels()
    Checking.check_status_code(response=list_parcel, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_parcel)


@allure.description("Получение информации о партии CД RussianPost")
def test_get_parcel_by_id(app, shared_data):
    random_parcel = app.parcel.get_parcel_id(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=random_parcel, expected_status_code=200)
    Checking.checking_json_key(response=random_parcel, expected_value=INFO.entity_parcel)


@allure.description("Редактирование партии СД RussianPost (Добавление заказов)")
@pytest.mark.parametrize("types", ["orders_courier", "orders_delivery_point", "orders_post_office", "orders_terminal"])
def test_add_order_in_parcel(app, connections, shared_data, types):
    for order in shared_data[types]:
        random_parcel = choice(shared_data["parcel_ids"])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=random_parcel, op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        assert order in connections.get_list_all_orders_in_parcel_for_parcel_id(parcel_id=random_parcel)


@allure.description("Редактирование партии СД RussianPost (Изменение даты отправки партии)")
def test_change_shipment_date(app, shared_data):
    parcel_id = choice(shared_data["parcel_ids"])
    shipment_date = app.parcel.patch_parcel_shipment_date(parcel_id=parcel_id, day=5)
    Checking.check_status_code(response=shipment_date, expected_status_code=200)
    new_date = shipment_date.json()["data"]["request"]["shipmentDate"]
    Checking.check_date_change(calendar_date=new_date, number_of_days=5)


@allure.description("Получение этикетки СД RussianPost")
def test_get_label(app, shared_data):
    for order_id in shared_data["order_ids_in_parcel"]:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД RussianPost")
def test_get_app(app, shared_data):
    acceptance = app.document.get_acceptance(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД RussianPost")
def test_get_documents(app, shared_data):
    documents = app.document.get_files(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание формы с этикетками партии СД RussianPost")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    forms_labels = app.forms.post_forms(parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=forms_labels, expected_status_code=201)
    Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)


@allure.description("Редактирование партии СД RussianPost (Удаление заказа из партии)")
def test_remove_order_in_parcel(app, connections, shared_data):
    remove_order = app.parcel.patch_parcel(op="remove", order_id=choice(shared_data["order_ids_in_parcel"]),
                                           parcel_id=choice(shared_data["parcel_ids"]))
    Checking.check_status_code(response=remove_order, expected_status_code=200)
    assert remove_order is not connections.get_list_all_orders_in_parcel()
