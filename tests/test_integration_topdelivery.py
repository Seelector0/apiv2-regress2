from utils.checking import Checking
from utils.enums.global_enums import INFO
from random import choice
import pytest
import allure


@allure.description("Создание магазина")
def test_create_integration_shop(app):
    new_shop = app.shop.post_shop()
    Checking.check_status_code(response=new_shop, expected_status_code=201)
    Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)
    get_new_shop = app.shop.get_shop_id(shop_id=new_shop.json()["id"])
    Checking.check_status_code(response=get_new_shop, expected_status_code=200)
    Checking.checking_json_value(response=get_new_shop, key_name="visibility", expected_value=True)


@allure.description("Создание склада")
def test_create_warehouse(app):
    new_warehouse = app.warehouse.post_warehouse()
    Checking.check_status_code(response=new_warehouse, expected_status_code=201)
    Checking.checking_json_key(response=new_warehouse, expected_value=INFO.created_entity)
    get_new_warehouse = app.warehouse.get_warehouse_id(warehouse_id=new_warehouse.json()["id"])
    Checking.check_status_code(response=get_new_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=get_new_warehouse, key_name="visibility", expected_value=True)


@allure.description("Подключение настроек СД TopDelivery")
def test_integration_delivery_services(app):
    topdelivery = app.service.delivery_services_topdelivery()
    Checking.check_status_code(response=topdelivery, expected_status_code=201)
    Checking.checking_json_key(response=topdelivery, expected_value=INFO.created_entity)
    get_topdelivery = app.service.get_delivery_services_code(code="TopDelivery")
    Checking.check_status_code(response=get_topdelivery, expected_status_code=200)
    Checking.checking_json_value(response=get_topdelivery, key_name="code", expected_value="TopDelivery")
    Checking.checking_json_value(response=get_topdelivery, key_name="credentials", field="visibility",
                                 expected_value=True)


@allure.description("Получение списка ПВЗ СД TopDelivery")
def test_delivery_service_points(app):
    delivery_service_points = app.info.delivery_service_points(delivery_service_code="TopDelivery")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="TopDelivery")


@allure.description("Получение списка точек сдачи СД TopDelivery")
def test_intake_offices(app):
    intake_offices = app.info.intake_offices(delivery_service_code="TopDelivery")
    Checking.check_status_code(response=intake_offices, expected_status_code=200)
    Checking.checking_in_list_json_value(response=intake_offices, key_name="deliveryServiceCode",
                                         expected_value="TopDelivery")


@allure.description("Получения сроков доставки по TopDelivery")
def test_delivery_time_schedules(app):
    delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="TopDelivery", day="today")
    Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
    Checking.checking_json_key(response=delivery_time_schedules, expected_value=["schedule", "intervals"])


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД TopDelivery")
def test_info_vats(app):
    info_vats = app.info.info_vats(delivery_service_code="TopDelivery")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.topdelivery_vats)


@allure.description("Получение актуального списка возможных статусов заказа СД TopDelivery")
def test_info_statuses(app):
    info_delivery_service_services = app.info.info_delivery_service_services(code="TopDelivery")
    Checking.check_status_code(response=info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=info_delivery_service_services,
                               expected_value=INFO.topdelivery_services)


@allure.description("Получение оферов в формате 'widget'")
def test_offers_format_widget(app):
    offers_widget = app.offers.get_offers(format_="widget")
    Checking.check_status_code(response=offers_widget, expected_status_code=200)
    Checking.check_delivery_services_in_widget_offers(response=offers_widget, delivery_service="TopDelivery")


@allure.description("Получение оферов по TopDelivery (Courier)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier",
                                           delivery_service_code="TopDelivery")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Получение оферов по TopDelivery (DeliveryPoint)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                  delivery_service_code="TopDelivery", delivery_point_number="55")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание Courier многоместного заказа по CД TopDelivery")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, payment_type, connections):
    new_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="TopDelivery",
                                           declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint многоместного заказа по CД TopDelivery")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_delivery_point(app, payment_type, connections):
    new_order = app.order.post_multi_order(payment_type=payment_type, type_ds="DeliveryPoint", service="TopDelivery",
                                           delivery_point_code="55", declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание Courier заказа по CД TopDelivery")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, payment_type, connections):
    new_order = app.order.post_order(payment_type=payment_type, type_ds="Courier", service="TopDelivery",
                                     declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint заказа по CД TopDelivery")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_delivery_point(app, payment_type, connections):
    new_order = app.order.post_order(payment_type=payment_type, type_ds="DeliveryPoint", service="TopDelivery",
                                     delivery_point_code="55", declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание многоместного заказа из одноместного")
def test_patch_single_order(app):
    list_order_id = app.order.getting_single_order_id_out_parcel()
    random_order_id = choice(list_order_id)
    single_order = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=single_order, expected_status_code=200)
    patch_single_order = app.order.patch_create_multy_order(order_id=random_order_id)
    Checking.check_status_code(response=patch_single_order, expected_status_code=200)
    Checking.checking_json_value(response=patch_single_order, key_name="status", expected_value="created")
    Checking.checking_json_value(response=patch_single_order, key_name="state", expected_value="succeeded")
    assert len(patch_single_order.json()["data"]["request"]["places"]) > \
           len(single_order.json()["data"]["request"]["places"])


@allure.description("Создание заказа из файла СД TopDelivery")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, file_extension, connections):
    new_order = app.order.post_import_order(delivery_services="topdelivery", file_extension=file_extension)
    Checking.check_status_code(response=new_order, expected_status_code=200)
    for order in new_order.json().values():
        connections.metaship.wait_create_order(order_id=order["id"])
        get_order_by_id = app.order.get_order_id(order_id=order["id"])
        Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
        Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Получение информации об истории изменения статусов заказа СД TopDelivery")
def test_order_status(app):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Удаление заказа TopDelivery")
def test_delete_order(app):
    random_order_id = choice(app.order.getting_all_order_id_out_parcel())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    get_order_by_id = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=404)


@allure.description("Получения этикеток СД TopDelivery вне партии")
@pytest.mark.parametrize("labels", [pytest.param("original", marks=pytest.mark.xfail), "termo"])
def test_get_labels_out_of_parcel(app, labels):
    for order_id in app.order.getting_all_order_id_out_parcel():
        label = app.document.get_label(order_id=order_id, type_="termo")
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД TopDelivery")
def test_order_details(app):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД TopDelivery")
def test_create_parcel(app):
    orders_id = app.order.getting_all_order_id_out_parcel()
    create_parcel = app.parcel.post_parcel(all_orders=True, order_id=orders_id)
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение этикеток СД TopDelivery")
@pytest.mark.parametrize("labels", [pytest.param("original", marks=pytest.mark.xfail), "termo"])
def test_get_label(app, labels):
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    for order_id in order_in_parcel:
        label = app.document.get_label(order_id=order_id, type_="termo")
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД TopDelivery")
def test_get_labels_from_parcel(app):
    orders_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    labels_from_parcel = app.document.post_labels(order_ids=orders_in_parcel)
    Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП СД TopDelivery")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД TopDelivery")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)
