from utils.checking import Checking
from random import choice, randint
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


@allure.description("Подключение настроек СД LPost")
def test_integration_delivery_services(app, token):
    cdek = app.service.delivery_services_l_post()
    Checking.check_status_code(response=cdek, expected_status_code=201)
    Checking.checking_json_key(response=cdek, expected_value=INFO.created_entity)
    get_cdek = app.service.get_delivery_services_code(code="LPost")
    Checking.check_status_code(response=get_cdek, expected_status_code=200)
    Checking.checking_json_value(response=get_cdek, key_name="code", expected_value="LPost")
    Checking.checking_json_value(response=get_cdek, key_name="credentials", field="visibility", expected_value=True)


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД LPost")
def test_info_vats(app, token):
    info_vats = app.info.info_vats(delivery_service_code="LPost")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.l_post_vats)


@allure.description("Получение актуального списка возможных сервисов заказа СД LPost")
def test_info_statuses(app, token):
    info_delivery_service_services = app.info.info_delivery_service_services(code="LPost")
    Checking.check_status_code(response=info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=info_delivery_service_services, expected_value=INFO.l_post_services)


@allure.description("Получение оферов по СД LPost (Courier)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type, token):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier", delivery_service_code="LPost")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Создание Courier многоместного заказа по CД LPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, token, payment_type):
    if payment_type == "Paid":
        new_multi_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="LPost",
                                                     declared_value=0, delivery_sum=0, price=0, dimension={
                                                         "length": randint(10, 30),
                                                         "width": randint(10, 30),
                                                         "height": randint(10, 30)
                                                     })
    else:
        new_multi_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="LPost",
                                                     declared_value=1500, price=1000, dimension={
                                                         "length": randint(10, 30),
                                                         "width": randint(10, 30),
                                                         "height": randint(10, 30)
                                                     })
    Checking.check_status_code(response=new_multi_order, expected_status_code=201)
    Checking.checking_json_key(response=new_multi_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_multi_order.json()["id"], sec=6)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание Courier заказа по СД LPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, token, payment_type):
    if payment_type == "Paid":
        new_order = app.order.post_order(payment_type=payment_type, type_ds="Courier", service="LPost", price=0,
                                         declared_value=0, delivery_sum=0)
    else:
        new_order = app.order.post_order(payment_type=payment_type, type_ds="Courier", service="LPost", price=1000,
                                         declared_value=1000)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"], sec=5)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Редактирование заказа СД LPost")
def test_editing_order(app, token):
    random_order = choice(app.order.getting_all_order_id_out_parcel())
    order_put = app.order.put_order(order_id=random_order, weight=5, length=12, width=14, height=11,
                                    declared_value=2500, family_name="Иванов")
    Checking.check_status_code(response=order_put, expected_status_code=200)
    Checking.checking_big_json(response=order_put, key_name="weight", expected_value=5)
    Checking.checking_big_json(response=order_put, key_name="payment", field="declaredValue", expected_value=2500)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="length", expected_value=12)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="width", expected_value=14)
    Checking.checking_big_json(response=order_put, key_name="dimension", field="height", expected_value=11)
    Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName", expected_value="Иванов")


@allure.description("Получение информации об истории изменения статусов заказа СД LPost")
def test_order_status(app, token):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Удаление заказа LPost")
def test_delete_order(app, token):
    random_order_id = choice(app.order.getting_all_order_id_out_parcel())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    get_order_by_id = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=get_order_by_id, expected_status_code=404)


@allure.description("Получение подробной информации о заказе СД LPost")
def test_order_details(app, token):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии CД LPost")
def test_create_parcel(app, token):
    orders_id = app.order.getting_all_order_id_out_parcel()
    create_parcel = app.parcel.post_parcel(all_orders=True, order_id=orders_id)
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение АПП СД LPost")
def test_get_app(app, token):
    app = app.document.get_acceptance()
    Checking.check_status_code(response=app, expected_status_code=200)


@allure.description("Получение документов СД LPost")
def test_get_documents(app, token):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)
