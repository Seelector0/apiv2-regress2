from utils.checking import Checking
from utils.enums.global_enums import INFO
from random import choice, randint
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


@allure.description("Подключение настроек службы доставки СД Cse")
def test_integration_delivery_services(app, token):
    cse = app.service.delivery_services_cse()
    Checking.check_status_code(response=cse, expected_status_code=201)
    Checking.checking_json_key(response=cse, expected_value=INFO.created_entity)
    get_cse = app.service.get_delivery_services_code(code="Cse")
    Checking.check_status_code(response=get_cse, expected_status_code=200)
    Checking.checking_json_value(response=get_cse, key_name="code", expected_value="Cse")
    Checking.checking_json_value(response=get_cse, key_name="credentials", field="visibility", expected_value=True)


@allure.description("Получение списка ПВЗ СД Cse")
def test_delivery_service_points(app, token):
    delivery_service_points = app.info.delivery_service_points(delivery_service_code="Cse")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="Cse")


@allure.description("Получение списка точек сдачи СД Cse")
def test_intake_offices(app, token):
    intake_offices = app.info.intake_offices(delivery_service_code="Cse")
    Checking.check_status_code(response=intake_offices, expected_status_code=200)
    Checking.checking_in_list_json_value(response=intake_offices, key_name="deliveryServiceCode", expected_value="Cse")


@allure.description("Получения сроков доставки по СД Cse")
def test_delivery_time_schedules(app, token):
    delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="Cse")
    Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
    Checking.checking_json_key(response=delivery_time_schedules, expected_value=["schedule", "intervals"])


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД Cse")
def test_info_vats(app, token):
    info_vats = app.info.info_vats(delivery_service_code="Cse")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.cse_vats)


@allure.description("Получение актуального списка возможных статусов заказа СД Cse")
def test_info_statuses(app, token):
    info_delivery_service_services = app.info.info_delivery_service_services(code="Cse")
    Checking.check_status_code(response=info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=info_delivery_service_services, expected_value=INFO.cse_services)


@allure.description("Получение оферов по СД Cse (Courier)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type, token):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier", delivery_service_code="Cse")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Создание Courier многоместного заказа по CД Cse")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, token, payment_type):
    new_multi_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="Cse",
                                                 tariff="64", declared_value=1500, dimension={
                                                        "length": randint(10, 30),
                                                        "width": randint(10, 50),
                                                        "height": randint(10, 50)
                                                 }, date_pickup=f"{datetime.date.today()}")
    Checking.check_status_code(response=new_multi_order, expected_status_code=201)
    Checking.checking_json_key(response=new_multi_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_multi_order.json()["id"], sec=10)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint многоместного заказа по CД Cse")
def test_create_multi_order_delivery_point(app, token):
    new_multi_order = app.order.post_multi_order(payment_type="Paid", type_ds="DeliveryPoint", service="Cse",
                                                 tariff="64", date_pickup=f"{datetime.date.today()}", dimension=
                                                 {
                                                    "length": randint(10, 30),
                                                    "width": randint(10, 50),
                                                    "height": randint(10, 50)
                                                 }, delivery_point_code="0299ca01-ed73-11e8-80c9-7cd30aebf951",
                                                 declared_value=1500)
    Checking.check_status_code(response=new_multi_order, expected_status_code=201)
    Checking.checking_json_key(response=new_multi_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_multi_order.json()["id"], sec=10)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Добавление items в многоместный заказ CД Cse")
@pytest.mark.skip("Падает с 400 кодом")
def test_patch_multi_order(app, token):
    choice_order_id = choice(app.order.getting_all_order_id_out_parcel())
    patch_order = app.order.patch_order_add_item(order_id=choice_order_id, path="add")
    Checking.check_status_code(response=patch_order, expected_status_code=200)
    Checking.checking_json_value(response=patch_order, key_name="status", expected_value="created")
    new_len_order_list = app.order.get_order_id(order_id=choice_order_id)
    Checking.check_status_code(response=new_len_order_list, expected_status_code=200)


@allure.description("Создание Courier заказа по СД Cse")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, token, payment_type):
    new_order = app.order.post_order(payment_type=payment_type, type_ds="Courier", service="Cse", tariff="64",
                                     date_pickup=f"{datetime.date.today()}", price=1000, declared_value=1500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"], sec=10)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint заказа по CД Cse")
def test_create_order_delivery_point(app, token):
    new_order = app.order.post_order(payment_type="Paid", type_ds="DeliveryPoint", service="Cse", tariff="64",
                                     date_pickup=f"{datetime.date.today()}", price=1000, declared_value=1500,
                                     delivery_point_code="0299ca01-ed73-11e8-80c9-7cd30aebf951")
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"], sec=12)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Получение информации об истории изменения статусов заказа СД Cse")
def test_order_status(app, token):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Удаление заказа СД Cse")
def test_delete_order(app, token):
    random_order_id = choice(app.order.getting_all_order_id_out_parcel())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    get_order_by_id = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=404)


@allure.description("Получения этикеток CД Cse вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, token, labels):
    for order_id in app.order.getting_all_order_id_out_parcel():
        label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение подробной информации о заказе СД Cse")
def test_order_details(app, token):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД Cse")
def test_create_parcel(app, token):
    orders_id = app.order.getting_all_order_id_out_parcel()
    create_parcel = app.parcel.post_parcel(order_id=choice(orders_id))
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Редактирование партии СД Cse (Добавление заказов)")
def test_add_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    for order in app.order.getting_all_order_id_out_parcel():
        old_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=parcel_id[0], op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        new_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        Checking.checking_sum_len_lists(old_list=old_list_order_in_parcel, new_list=new_list_order_in_parcel)


@allure.description("Получение этикеток СД Cse")
def test_get_label(app, token):
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=app.parcel.getting_list_of_parcels_ids()[0])
    for order_id in order_in_parcel:
        label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение АПП СД Cse")
def test_get_app(app, token):
    app = app.document.get_acceptance()
    Checking.check_status_code(response=app, expected_status_code=200)


@allure.description("Получение документов СД Cse")
def test_get_documents(app, token):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Редактирование партии СД Cse (Удаление заказа)")
def test_remove_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    old_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    parcel_remove = app.parcel.patch_parcel(order_id=choice(order_in_parcel), parcel_id=parcel_id[0], op="remove")
    new_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    Checking.check_status_code(response=parcel_remove, expected_status_code=200)
    Checking.checking_difference_len_lists(old_list=old_list_order, new_list=new_list_order)
