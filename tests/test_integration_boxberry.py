from utils.checking import Checking
from random import choice
import pytest
import allure

# Todo разобраться с widget offers, добавить создание многоместных заказов после того как решиться вопрос с этикетками


@allure.description("Создание магазина")
def test_create_integration_shop(app, token):
    result_new_shop = app.shop.create_shop()
    Checking.check_status_code(response=result_new_shop, expected_status_code=201)
    Checking.checking_json_key(response=result_new_shop, expected_value=["id", "type", "url", "status"])
    result_get_new_shop = app.shop.get_shop_by_id(shop_id=result_new_shop.json()["id"])
    Checking.check_status_code(response=result_get_new_shop, expected_status_code=200)
    Checking.checking_json_value(response=result_get_new_shop, key_name="visibility", expected_value=True)


@allure.description("Создание склада")
def test_create_warehouse(app, token):
    result_new_warehouse = app.warehouse.create_warehouse()
    Checking.check_status_code(response=result_new_warehouse, expected_status_code=201)
    Checking.checking_json_key(response=result_new_warehouse, expected_value=["id", "type", "url", "status"])
    result_get_new_warehouse = app.warehouse.get_warehouse_by_id(warehouse_id=result_new_warehouse.json()["id"])
    Checking.check_status_code(response=result_get_new_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=result_get_new_warehouse, key_name="visibility", expected_value=True)


@allure.description("Подключение настроек СД Boxberry")
def test_integration_delivery_services(app, token):
    result_boxberry = app.service.delivery_services_boxberry()
    Checking.check_status_code(response=result_boxberry, expected_status_code=201)
    Checking.checking_json_key(response=result_boxberry, expected_value=["id", "type", "url", "status"])
    result_get_boxberry = app.service.get_delivery_services_code(code="Boxberry")
    Checking.check_status_code(response=result_get_boxberry, expected_status_code=200)
    Checking.checking_json_value(response=result_get_boxberry, key_name="code", expected_value="Boxberry")
    Checking.checking_json_value(response=result_get_boxberry, key_name="credentials", field="visibility",
                                 expected_value=True)


@allure.description("Получение списка ПВЗ СД Boxberry")
def test_delivery_service_points(app, token):
    result_delivery_service_points = app.info.delivery_service_points(delivery_service_code="Boxberry")
    Checking.check_status_code(response=result_delivery_service_points, expected_status_code=200)
    Checking.checking_in_list_json_value(response=result_delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="Boxberry")


@allure.description("Получение списка точек сдачи СД Boxberry")
def test_intake_offices(app, token):
    result_intake_offices = app.info.intake_offices(delivery_service_code="Boxberry")
    Checking.check_status_code(response=result_intake_offices, expected_status_code=200)
    Checking.checking_in_list_json_value(response=result_intake_offices, key_name="deliveryServiceCode",
                                         expected_value="Boxberry")


@allure.description("Получения сроков доставки по СД Boxberry")
def test_delivery_time_schedules(app, token):
    result_delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="Boxberry")
    Checking.check_status_code(response=result_delivery_time_schedules, expected_status_code=200)
    Checking.checking_json_key(response=result_delivery_time_schedules, expected_value=["schedule", "intervals"])


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД Boxberry")
def test_info_vats(app, token):
    result_info_vats = app.info.info_vats(delivery_service_code="Boxberry")
    Checking.check_status_code(response=result_info_vats, expected_status_code=200)
    Checking.checking_json_key(response=result_info_vats, expected_value=[{"code": "NO_VAT", "name": "Без НДС"},
                                                                          {"code": "0", "name": "НДС 0%"},
                                                                          {"code": "10", "name": "НДС 10%"},
                                                                          {"code": "20", "name": "НДС 20%"}])


@allure.description("Получение актуального списка возможных сервисов заказа СД Boxberry")
def test_info_statuses(app, token):
    result_info_delivery_service_services = app.info.info_delivery_service_services(code="Boxberry")
    Checking.check_status_code(response=result_info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=result_info_delivery_service_services, expected_value=[
        {"name": "not-open",
         "title": "Не вскрывать до получения оплаты с клиента",
         "description": "Не вскрывать до получения оплаты с клиента"},
        {"name": "open-test",
         "title": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности",
         "description": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности"},
        {"name": "partial-sale",
         "title": "Частичная реализация",
         "description": "Частичная реализация"}])


@allure.description("Получение оферов по СД Boxberry (Courier)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type, token):
    result_offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier",
                                                  delivery_service_code="Boxberry")
    Checking.check_status_code(response=result_offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=result_offers_courier, expected_value=["Courier"])


@allure.description("Получение оферов по СД Boxberry (DeliveryPoint)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type, token):
    result_offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                         delivery_service_code="Boxberry")
    Checking.check_status_code(response=result_offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=result_offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание Courier многоместного заказа по CД Boxberry")
@pytest.mark.skip("Проблемы с печатью этикеток для многоместного заказа")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, token, payment_type):
    result_order = app.order.create_multi_order(payment_type=payment_type, type_ds="Courier", service="Boxberry",
                                                declared_value=1500)
    Checking.check_status_code(response=result_order, expected_status_code=201)
    Checking.checking_json_key(response=result_order, expected_value=["id", "type", "url", "status"])
    result_get_order_by_id = app.order.get_order_by_id(order_id=result_order.json()["id"])
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint многоместного заказа по CД Boxberry")
@pytest.mark.skip("Проблемы с печатью этикеток для многоместного заказа")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_multi_delivery_point(app, token, payment_type):
    result_order = app.order.create_multi_order(payment_type=payment_type, type_ds="DeliveryPoint", service="Boxberry",
                                                delivery_point_code="00199", declared_value=1500)
    Checking.check_status_code(response=result_order, expected_status_code=201)
    Checking.checking_json_key(response=result_order, expected_value=["id", "type", "url", "status"])
    result_get_order_by_id = app.order.get_order_by_id(order_id=result_order.json()["id"])
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание Courier заказа по CД Boxberry")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, token, payment_type):
    result_order = app.order.create_order(payment_type=payment_type, type_ds="Courier", service="Boxberry", price=1000,
                                          declared_value=1500)
    Checking.check_status_code(response=result_order, expected_status_code=201)
    Checking.checking_json_key(response=result_order, expected_value=["id", "type", "url", "status"])
    result_get_order_by_id = app.order.get_order_by_id(order_id=result_order.json()["id"])
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint заказа по CД Boxberry")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_delivery_point(app, token, payment_type):
    result_order = app.order.create_order(payment_type=payment_type,
                                          type_ds="DeliveryPoint", service="Boxberry", delivery_point_code="00199",
                                          price=1000, declared_value=1500)
    Checking.check_status_code(response=result_order, expected_status_code=201)
    Checking.checking_json_key(response=result_order, expected_value=["id", "type", "url", "status"])
    result_get_order_by_id = app.order.get_order_by_id(order_id=result_order.json()["id"])
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Удаление заказа CД Boxberry")
def test_delete_order(app, token):
    orders_id_list = app.order.get_orders_id()
    random_order_id = choice(orders_id_list)
    result_delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=result_delete_order, expected_status_code=204)
    result_get_order_by_id = app.order.get_order_by_id(order_id=random_order_id)
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=404)


@allure.description("Получения этикетки Boxberry вне партии")
def test_get_label_out_of_parcel(app, token):
    list_order_id = app.order.get_orders_id()
    for order_id in list_order_id:
        result_label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=result_label, expected_status_code=200)


@allure.description("Попытка редактирования заказа СД Boxberry")
def test_editing_order(app, token):
    order_list_id = app.order.get_orders_id()
    result_order_put = app.order.update_order(order_id=choice(order_list_id), weight=5, length=12, width=14, height=11,
                                              declared_value=2500, family_name="Иванов")
    Checking.check_status_code(response=result_order_put, expected_status_code=400)


@allure.description("Получение информации об истории изменения статусов заказа CД Boxberry")
def test_order_status(app, token):
    order_list_id = app.order.get_orders_id()
    for order_id in order_list_id:
        result_order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=result_order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=result_order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе CД Boxberry")
def test_order_details(app, token):
    order_list_id = app.order.get_orders_id()
    for order_id in order_list_id:
        result_order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=result_order_details, expected_status_code=200)
        Checking.checking_json_key(response=result_order_details, expected_value=["returnItems", "returnReason",
                                                                                  "delayReason", "paymentType",
                                                                                  "pickupDate", "declaredDeliveryDate",
                                                                                  "storageDateEnd"])


@allure.description("Создание партии CД Boxberry")
def test_create_parcel(app, token):
    orders_id = app.order.get_orders_id()
    result_create_parcel = app.parcel.create_parcel(all_orders=True, order_id=orders_id)
    Checking.check_status_code(response=result_create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=result_create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Редактирование партии CД Boxberry(Попытка изменения даты отправки партии)")
def test_change_shipment_date(app, token):
    parcel_id = app.parcel.get_parcels_id()
    result_shipment_date = app.parcel.change_parcel_shipment_date(parcel_id=parcel_id[0], day=5)
    Checking.check_status_code(response=result_shipment_date, expected_status_code=422)


@allure.description("Получение этикетки CД Boxberry")
def test_get_labels(app, token):
    parcel_id = app.parcel.get_parcels_id()
    result_order_in_parcel = app.parcel.get_order_in_parcel(parcel_id=parcel_id[0])
    for order_id in result_order_in_parcel:
        result_label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=result_label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД Boxberry")
def test_get_labels_from_parcel(app, token):
    parcel_id = app.parcel.get_parcels_id()
    order_in_parcel = app.parcel.get_order_in_parcel(parcel_id=parcel_id[0])
    result_labels_from_parcel = app.document.get_labels_from_parcel(parcel_id=parcel_id[0], order_ids=order_in_parcel)
    Checking.check_status_code(response=result_labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП CД Boxberry")
def test_get_app(app, token):
    result_app = app.document.get_app()
    Checking.check_status_code(response=result_app, expected_status_code=200)


@allure.description("Получение документов CД Boxberry")
def test_get_documents(app, token):
    result_documents = app.document.get_documents()
    Checking.check_status_code(response=result_documents, expected_status_code=200)


@allure.description("Попытка Редактирование партии CД Boxberry(Удаление заказа)")
def test_remove_order_in_parcel(app, token):
    parcel_id = app.parcel.get_parcels_id()
    result_order_in_parcel = app.parcel.get_order_in_parcel(parcel_id=parcel_id[0])
    result_parcel_remove = app.parcel.change_parcel_orders(order_id=choice(result_order_in_parcel),
                                                           parcel_id=parcel_id[0], op="remove")
    Checking.check_status_code(response=result_parcel_remove, expected_status_code=422)
