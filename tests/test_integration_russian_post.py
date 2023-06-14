from utils.checking import Checking
from random import choice
from utils.enums.global_enums import INFO
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


@allure.description("Подключение настроек службы доставки СД Почта России")
def test_integration_delivery_services(app, token):
    russian_post = app.service.delivery_services_russian_post()
    Checking.check_status_code(response=russian_post, expected_status_code=201)
    Checking.checking_json_key(response=russian_post, expected_value=INFO.created_entity)
    get_russian_post = app.service.get_delivery_services_code(code="RussianPost")
    Checking.check_status_code(response=get_russian_post, expected_status_code=200)
    Checking.checking_json_value(response=get_russian_post, key_name="code", expected_value="RussianPost")
    Checking.checking_json_value(response=get_russian_post, key_name="credentials", field="visibility",
                                 expected_value=True)


@allure.description("Получение списка ПВЗ СД Почта России")
def test_delivery_service_points(app, token):
    delivery_service_points = app.info.delivery_service_points(delivery_service_code="RussianPost")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="RussianPost")


@allure.description("Получение списка точек сдачи СД Почты России")
def test_intake_offices(app, token):
    intake_offices = app.info.intake_offices(delivery_service_code="RussianPost")
    Checking.check_status_code(response=intake_offices, expected_status_code=200)
    Checking.checking_in_list_json_value(response=intake_offices, key_name="deliveryServiceCode",
                                         expected_value="RussianPost")


@allure.description("Получения сроков доставки по СД Почта России")
def test_delivery_time_schedules(app, token):
    delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="RussianPost")
    Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
    Checking.checking_json_key(response=delivery_time_schedules, expected_value=["schedule", "intervals"])


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД Почта России")
def test_info_vats(app, token):
    info_vats = app.info.info_vats(delivery_service_code="RussianPost")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.rp_vats)


@allure.description("Получение актуального списка возможных статусов заказа СД Почта России")
def test_info_statuses(app, token):
    info_delivery_service_services = app.info.info_delivery_service_services(code="RussianPost")
    Checking.check_status_code(response=info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=info_delivery_service_services, expected_value=INFO.rp_services)


@allure.description("Получение оферов по СД Почта России (Courier)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type, token):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier",
                                           delivery_service_code="RussianPost")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Получение оферов по СД Почта России (DeliveryPoint)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type, token):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                  delivery_service_code="RussianPost")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["PostOffice"])


@allure.description("Получение оферов по СД Почта России (PostOffice)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_russian_post(app, payment_type, token):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="PostOffice",
                                                  delivery_service_code="RussianPost")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["PostOffice"])


@allure.description("Создание Courier заказа по СД Почта России")
def test_create_order_courier(app, token, connections):
    new_order = app.order.post_order(payment_type="Paid", type_ds="Courier", service="RussianPost",
                                     tariff=choice(INFO.rp_courier_tariffs), declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint заказа по СД Почта России")
def test_create_delivery_point(app, token, connections):
    new_order = app.order.post_order(payment_type="Paid", length=15, width=15, height=15, type_ds="DeliveryPoint",
                                     service="RussianPost", tariff=INFO.rp_po_tariffs[0], delivery_point_code="914841",
                                     declared_value=1000)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание PostOffice заказа по СД Почта России")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_post_office(app, payment_type, token, connections):
    new_order = app.order.post_order(payment_type=payment_type, type_ds="PostOffice", service="RussianPost",
                                     tariff=choice(INFO.rp_po_tariffs), declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Редактирование заказа СД Почта России")
def test_editing_order(app, token):
    random_order = choice(app.order.getting_all_order_id_out_parcel())
    order_put = app.order.put_order(order_id=random_order, weight=5, length=12, width=14, height=11,
                                    family_name="Иванов")
    Checking.check_status_code(response=order_put, expected_status_code=200)
    Checking.checking_big_json(response=order_put, key_name="weight", expected_value=5)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="length", expected_value=12)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="width", expected_value=14)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="height", expected_value=11)
    Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName", expected_value="Иванов")


@allure.description("Редактирование веса в заказе СД Почта России")
def test_patch_order_weight(app, token):
    random_order = choice(app.order.getting_all_order_id_out_parcel())
    order_patch = app.order.patch_order(order_id=random_order, path="weight", weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Создание заказа из файла СД Почты России")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, token, file_extension, connections):
    new_orders = app.order.post_import_order(delivery_services="russian_post", file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    for order in new_orders.json().values():
        connections.metaship.wait_create_order(order_id=order["id"])
        get_order_by_id = app.order.get_order_id(order_id=order["id"])
        Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
        Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание заказа из файла формата Почты России")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file_format_russian_post(app, token, file_extension, connections):
    new_orders = app.order.post_import_order_format_russian_post(file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    for order in new_orders.json().values():
        connections.metaship.wait_create_order(order_id=order["id"])
        get_order_by_id = app.order.get_order_id(order_id=order["id"])
        Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
        Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Удаление заказа СД Почта России")
def test_delete_order(app, token):
    random_order_id = choice(app.order.getting_all_order_id_out_parcel())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    get_order_by_id = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=404)


@allure.description("Получение информации об истории изменения статусов заказа СД Почта России")
def test_order_status(app, token):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе СД Почта России")
def test_order_details(app, token):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Почта России")
def test_create_parcel(app, token):
    orders_id = app.order.getting_all_order_id_out_parcel()
    create_parcel = app.parcel.post_parcel(order_id=choice(orders_id))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Редактирование партии СД Почта России (Добавление заказов)")
def test_add_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    for order in app.order.getting_all_order_id_out_parcel():
        old_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        new_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        Checking.checking_sum_len_lists(old_list=old_list_order_in_parcel, new_list=new_list_order_in_parcel)


@allure.description("Редактирование партии СД Почта России (Изменение даты отправки партии)")
def test_change_shipment_date(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    shipment_date = app.parcel.patch_parcel_shipment_date(parcel_id=parcel_id[0], day=5)
    Checking.check_status_code(response=shipment_date, expected_status_code=200)
    new_date = shipment_date.json()["data"]["request"]["shipmentDate"]
    Checking.check_date_change(calendar_date=new_date, number_of_days=5)


@allure.description("Получение этикетки СД Почта России")
def test_get_label(app, token):
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    for order_id in order_in_parcel:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД Почта России")
def test_get_app(app, token):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД Почта России")
def test_get_documents(app, token):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Редактирование партии СД Почта России (Удаление заказа из партии)")
def test_remove_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    old_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    parcel_remove = app.parcel.patch_parcel(order_id=choice(old_list_order), parcel_id=parcel_id[0], op="remove")
    new_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    Checking.check_status_code(response=parcel_remove, expected_status_code=200)
    Checking.checking_difference_len_lists(old_list=old_list_order, new_list=new_list_order)
