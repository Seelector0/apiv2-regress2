from utils.checking import Checking
from utils.enums.global_enums import INFO
from random import choice, randrange
import datetime
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


@allure.description("Подключение настроек СД Dpd")
def test_integration_delivery_services(app, token):
    dpd = app.service.delivery_services_dpd()
    Checking.check_status_code(response=dpd, expected_status_code=201)
    Checking.checking_json_key(response=dpd, expected_value=INFO.created_entity)
    get_dpd = app.service.get_delivery_services_code(code="Dpd")
    Checking.check_status_code(response=get_dpd, expected_status_code=200)
    Checking.checking_json_value(response=get_dpd, key_name="code", expected_value="Dpd")
    Checking.checking_json_value(response=get_dpd, key_name="credentials", field="visibility", expected_value=True)


@allure.description("Получение списка ПВЗ  СД Dpd")
def test_delivery_service_points(app, token):
    delivery_service_points = app.info.delivery_service_points(delivery_service_code="Dpd")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="Dpd")


@allure.description("Получения сроков доставки по СД Dpd")
def test_delivery_time_schedules(app, token):
    delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="Dpd")
    Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
    Checking.checking_json_key(response=delivery_time_schedules, expected_value=["schedule", "intervals"])


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД Dpd")
def test_info_vats(app, token):
    info_vats = app.info.info_vats(delivery_service_code="Dpd")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.dpd_vats)


@allure.description("Получение актуального списка возможных сервисов заказа СД Dpd")
def test_info_statuses(app, token):
    info_delivery_service_services = app.info.info_delivery_service_services(code="Dpd")
    Checking.check_status_code(response=info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=info_delivery_service_services, expected_value=INFO.dpd_services)


@allure.description("Получение оферов в формате 'widget'")
def test_offers_format_widget(app, token):
    offers_widget = app.offers.get_offers(format_="widget")
    Checking.check_status_code(response=offers_widget, expected_status_code=200)
    Checking.check_delivery_services_in_widget_offers(response=offers_widget, delivery_service="Dpd")


@allure.description("Получение оферов по СД Dpd (Courier)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, token, payment_type):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier", delivery_service_code="Dpd")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Получение оферов по СД Dpd (DeliveryPoint)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type, token):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                  delivery_service_code="Dpd")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание Courier многоместного заказа по CД Dpd")
def test_create_multi_order_courier(app, token):
    new_multi_order = app.order.post_multi_order(payment_type="Paid", type_ds="Courier", service="Dpd",
                                                 tariff=choice(INFO.dpd_courier_tariffs),
                                                 date_pickup=f"{datetime.date.today()}", pickup_time_period="9-18",
                                                 declared_value=1500)
    Checking.check_status_code(response=new_multi_order, expected_status_code=201)
    Checking.checking_json_key(response=new_multi_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_multi_order.json()["id"], sec=12)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint многоместного заказа по CД Dpd")
def test_create_multi_order_delivery_point(app, token):
    new_order = app.order.post_multi_order(payment_type="Paid", type_ds="DeliveryPoint", service="Dpd",
                                           tariff=choice(INFO.dpd_ds_tariffs), date_pickup=f"{datetime.date.today()}",
                                           pickup_time_period="9-18", delivery_point_code="007K", declared_value=1500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"], sec=6)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание Courier заказа по CД Dpd")
def test_create_order_courier(app, token):
    new_order = app.order.post_order(payment_type="Paid", type_ds="Courier", service="Dpd",
                                     barcode=f"{randrange(100000000, 999999999)}",
                                     tariff=choice(INFO.dpd_courier_tariffs), date_pickup=f"{datetime.date.today()}",
                                     pickup_time_period="9-18", price=1000, declared_value=1500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"], sec=8)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint заказа по CД Dpd")
def test_create_order_delivery_point(app, token):
    new_order = app.order.post_order(payment_type="Paid", type_ds="DeliveryPoint", service="Dpd",
                                     barcode=f"{randrange(100000000, 999999999)}", tariff=choice(INFO.dpd_ds_tariffs),
                                     date_pickup=f"{datetime.date.today()}", pickup_time_period="9-18",
                                     delivery_point_code="007K", price=1000, declared_value=1500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"], sec=6)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Получение информации об истории изменения статусов заказа СД Dpd")
def test_order_status(app, token):
    order_list_id = app.order.getting_all_order_id_out_parcel()
    for order_id in order_list_id:
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Редактирование веса в заказе СД Dpd")
def test_patch_order_weight(app, token):
    random_order = choice(app.order.getting_all_order_id_out_parcel())
    order_patch = app.order.patch_order(order_id=random_order, path="weight", weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Удаление заказа СД Dpd")
def test_delete_order(app, token):
    random_order_id = choice(app.order.getting_all_order_id_out_parcel())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    get_order_by_id = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=404)


@allure.description("Получения этикеток CД Dpd вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, token, labels):
    order_out_parcel = app.order.getting_all_order_id_out_parcel()
    for order_id in order_out_parcel:
        label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получения оригинальных этикеток CД Dpd в формате A5, A6 вне партии")
@pytest.mark.parametrize("format_", ["A5", "A6"])
def test_get_original_labels_out_of_parcel(app, token, format_):
    order_out_parcel = app.order.getting_all_order_id_out_parcel()
    for order_id in order_out_parcel:
        label = app.document.get_label(order_id=order_id, size=True, format_=format_)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД Dpd")
def test_order_details(app, token):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Dpd")
def test_create_parcel(app, token):
    orders_id = app.order.getting_all_order_id_out_parcel()
    create_parcel = app.parcel.post_parcel(order_id=choice(orders_id))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Редактирование партии СД Dpd (Добавление заказов)")
def test_add_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    for order in app.order.getting_all_order_id_out_parcel():
        old_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        new_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        Checking.checking_sum_len_lists(old_list=old_list_order_in_parcel, new_list=new_list_order_in_parcel)


@allure.description("Редактирование веса заказа в партии СД Dpd")
def test_patch_weight_random_order_in_parcel(app, token):
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    order_patch = app.order.patch_order(order_id=choice(order_in_parcel), path="weight", weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Получение этикеток СД Dpd")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_label(app, token, labels):
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    for order_id in order_in_parcel:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получения оригинальных этикеток CД Dpd в формате A5, A6")
@pytest.mark.parametrize("format_", ["A5", "A6"])
def test_get_original_labels(app, token, format_):
    order_in_parcel = app.order.getting_all_order_in_parcel()
    for order_id in order_in_parcel:
        label = app.document.get_label(order_id=order_id, size=True, format_=format_)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД Dpd")
def test_get_app(app, token):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД Dpd")
def test_get_documents(app, token):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Редактирование партии СД Dpd (Удаление заказа)")
def test_remove_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    old_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    parcel_remove = app.parcel.patch_parcel(order_id=choice(old_list_order), parcel_id=parcel_id[0], op="remove")
    new_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    Checking.check_status_code(response=parcel_remove, expected_status_code=200)
    Checking.checking_difference_len_lists(old_list=old_list_order, new_list=new_list_order)
