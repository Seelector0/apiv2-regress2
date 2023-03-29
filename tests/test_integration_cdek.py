from utils.checking import Checking
from utils.enums.global_enums import OtherInfo
from random import choice
import pytest
import allure


# Todo разобраться с widget offers


@allure.description("Создание магазина")
def test_create_integration_shop(app, token):
    result_new_shop = app.shop.post_shop()
    Checking.check_status_code(response=result_new_shop, expected_status_code=201)
    Checking.checking_json_key(response=result_new_shop, expected_value=["id", "type", "url", "status"])
    result_get_new_shop = app.shop.get_shop_id(shop_id=result_new_shop.json()["id"])
    Checking.check_status_code(response=result_get_new_shop, expected_status_code=200)
    Checking.checking_json_value(response=result_get_new_shop, key_name="visibility", expected_value=True)


@allure.description("Создание склада")
def test_create_warehouse(app, token):
    result_new_warehouse = app.warehouse.post_warehouse()
    Checking.check_status_code(response=result_new_warehouse, expected_status_code=201)
    Checking.checking_json_key(response=result_new_warehouse, expected_value=["id", "type", "url", "status"])
    result_get_new_warehouse = app.warehouse.get_warehouse_id(warehouse_id=result_new_warehouse.json()["id"])
    Checking.check_status_code(response=result_get_new_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=result_get_new_warehouse, key_name="visibility", expected_value=True)


@allure.description("Подключение настроек СД СДЭК")
def test_integration_delivery_services(app, token):
    result_cdek = app.service.delivery_services_cdek()
    Checking.check_status_code(response=result_cdek, expected_status_code=201)
    Checking.checking_json_key(response=result_cdek, expected_value=["id", "type", "url", "status"])
    result_get_cdek = app.service.get_delivery_services_code(code="Cdek")
    Checking.check_status_code(response=result_get_cdek, expected_status_code=200)
    Checking.checking_json_value(response=result_get_cdek, key_name="code", expected_value="Cdek")
    Checking.checking_json_value(response=result_get_cdek, key_name="credentials", field="visibility",
                                 expected_value=True)


@allure.description("Получение списка ПВЗ СД СДЭК")
def test_delivery_service_points(app, token):
    result_delivery_service_points = app.info.delivery_service_points(delivery_service_code="Cdek")
    Checking.check_status_code(response=result_delivery_service_points, expected_status_code=200)
    Checking.checking_in_list_json_value(response=result_delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="Cdek")


@allure.description("Получение списка точек сдачи СД СДЭК")
def test_intake_offices(app, token):
    result_intake_offices = app.info.intake_offices(delivery_service_code="Cdek")
    Checking.check_status_code(response=result_intake_offices, expected_status_code=200)
    Checking.checking_in_list_json_value(response=result_intake_offices, key_name="deliveryServiceCode",
                                         expected_value="Cdek")


@allure.description("Получения сроков доставки по СД СДЭК")
def test_delivery_time_schedules(app, token):
    result_delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="Cdek")
    Checking.check_status_code(response=result_delivery_time_schedules, expected_status_code=200)
    Checking.checking_json_key(response=result_delivery_time_schedules, expected_value=["schedule", "intervals"])


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД СДЭК")
def test_info_vats(app, token):
    result_info_vats = app.info.info_vats(delivery_service_code="Cdek")
    Checking.check_status_code(response=result_info_vats, expected_status_code=200)
    Checking.checking_json_key(response=result_info_vats, expected_value=OtherInfo.CDEK_VATS.value)


@allure.description("Получение актуального списка возможных сервисов заказа СД СДЭК")
def test_info_statuses(app, token):
    result_info_delivery_service_services = app.info.info_delivery_service_services(code="Cdek")
    Checking.check_status_code(response=result_info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=result_info_delivery_service_services,
                               expected_value=OtherInfo.CDEK_SERVICES.value)


@allure.description("Получение оферов по СД СДЭК (Courier)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type, token):
    result_offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier",
                                                  delivery_service_code="Cdek")
    Checking.check_status_code(response=result_offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=result_offers_courier, expected_value=["Courier"])


@allure.description("Получение оферов по СД Cdek (DeliveryPoint)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type, token):
    result_offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                         delivery_service_code="Cdek")
    Checking.check_status_code(response=result_offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=result_offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание Courier многоместного заказа по CД СДЭК")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, token, payment_type):
    result_multi_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="Cdek",
                                                    tariff=choice(OtherInfo.CDEK_COURIER_TARIFFS.value),
                                                    declared_value=1500)
    Checking.check_status_code(response=result_multi_order, expected_status_code=201)
    Checking.checking_json_key(response=result_multi_order, expected_value=["id", "type", "url", "status"])
    result_get_order_by_id = app.order.get_order_id(order_id=result_multi_order.json()["id"], sec=7)
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint многоместного заказа по CД СДЭК")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_delivery_point(app, token, payment_type):
    result_multi_order = app.order.post_multi_order(payment_type=payment_type, type_ds="DeliveryPoint",
                                                    service="Cdek", tariff=choice(OtherInfo.CDEK_DS_TARIFFS.value),
                                                    delivery_point_code="VNG2", declared_value=1500)
    Checking.check_status_code(response=result_multi_order, expected_status_code=201)
    Checking.checking_json_key(response=result_multi_order, expected_value=["id", "type", "url", "status"])
    result_get_order_by_id = app.order.get_order_id(order_id=result_multi_order.json()["id"], sec=6)
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Добавление items в многоместный заказ СД СДЭК")
def test_patch_multi_order(app, token):
    list_order_id = app.order.getting_order_id_out_parcel()
    choice_order_id = choice(list_order_id)
    old_len_order_list = app.order.get_order_id(order_id=choice_order_id)
    result_patch_order = app.order.patch_order(order_id=choice_order_id, path="places")
    Checking.check_status_code(response=result_patch_order, expected_status_code=200)
    Checking.checking_json_value(response=result_patch_order, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_patch_order, key_name="state",
                                 expected_value="editing-external-processing")
    new_len_order_list = app.order.get_order_id(order_id=choice_order_id, sec=7)
    Checking.check_status_code(response=new_len_order_list, expected_status_code=200)
    Checking.checking_json_value(response=new_len_order_list, key_name="status", expected_value="created")
    Checking.checking_json_value(response=new_len_order_list, key_name="state", expected_value="succeeded")
    Checking.checking_sum_len_lists(old_list=old_len_order_list.json()["data"]["request"]["places"],
                                    new_list=new_len_order_list.json()["data"]["request"]["places"])


@allure.description("Создание Courier заказа по CД СДЭК")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, token, payment_type):
    result_order = app.order.post_order(payment_type=payment_type, type_ds="Courier", service="Cdek",
                                        tariff=choice(OtherInfo.CDEK_COURIER_TARIFFS.value), price=1000,
                                        declared_value=1500)
    Checking.check_status_code(response=result_order, expected_status_code=201)
    Checking.checking_json_key(response=result_order, expected_value=["id", "type", "url", "status"])
    result_get_order_by_id = app.order.get_order_id(order_id=result_order.json()["id"], sec=7)
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание DeliveryPoint заказа по CД СДЭК")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_delivery_point(app, token, payment_type):
    result_order = app.order.post_order(payment_type=payment_type, type_ds="DeliveryPoint", service="Cdek",
                                        tariff=choice(OtherInfo.CDEK_DS_TARIFFS.value), delivery_point_code="VNG2",
                                        price=1000, declared_value=1500)
    Checking.check_status_code(response=result_order, expected_status_code=201)
    Checking.checking_json_key(response=result_order, expected_value=["id", "type", "url", "status"])
    result_get_order_by_id = app.order.get_order_id(order_id=result_order.json()["id"], sec=7)
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Получение информации об истории изменения статусов заказа СД СДЭК")
def test_order_status(app, token):
    order_list_id = app.order.getting_order_id_out_parcel()
    for order_id in order_list_id:
        result_order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=result_order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=result_order_status, key_name="status", expected_value="created")


@allure.description("Удаление заказа СД СДЭК")
def test_delete_order(app, token):
    orders_id_list = app.order.getting_order_id_out_parcel()
    random_order_id = choice(orders_id_list)
    result_delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=result_delete_order, expected_status_code=204)
    result_get_order_by_id = app.order.get_order_id(order_id=random_order_id)
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=404)


@allure.description("Получения этикеток CД СДЭК вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, token, labels):
    list_order_id = app.order.getting_order_id_out_parcel()
    for order_id in list_order_id:
        result_label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=result_label, expected_status_code=200)


@allure.description("Попытка редактирования заказа СД СДЭК")
def test_editing_order(app, token):
    order_list_id = app.order.getting_order_id_out_parcel()
    result_order_put = app.order.put_order(order_id=choice(order_list_id), weight=5, length=12, width=14, height=11,
                                           declared_value=2500, family_name="Иванов")
    Checking.check_status_code(response=result_order_put, expected_status_code=400)


@allure.description("Получение подробной информации о заказе СД СДЭК")
def test_order_details(app, token):
    order_list_id = app.order.getting_order_id_out_parcel()
    for order_id in order_list_id:
        result_order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=result_order_details, expected_status_code=200)
        Checking.checking_json_key(response=result_order_details, expected_value=OtherInfo.DETAILS.value)


@allure.description("Создание партии СД СДЭК")
def test_create_parcel(app, token):
    orders_id = app.order.getting_order_id_out_parcel()
    result_create_parcel = app.parcel.post_parcel(order_id=choice(orders_id))
    Checking.check_status_code(response=result_create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=result_create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Редактирование партии СД СДЭК (Добавление заказов)")
def test_add_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    orders_id = app.order.getting_order_id_out_parcel()
    for order in orders_id:
        old_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        result_parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=parcel_id[0], op="add")
        Checking.check_status_code(response=result_parcel_add, expected_status_code=200)
        new_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
        Checking.checking_sum_len_lists(old_list=old_list_order_in_parcel, new_list=new_list_order_in_parcel)


@allure.description("Редактирование партии СД СДЭК (Попытка изменение даты отправки партии)")
def test_change_shipment_date(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    result_shipment_date = app.parcel.patch_parcel_shipment_date(parcel_id=parcel_id[0], day=5)
    Checking.check_status_code(response=result_shipment_date, expected_status_code=422)


@allure.description("Получение этикеток СД СДЭК")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_label(app, token, labels):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    result_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    for order_id in result_order_in_parcel:
        result_label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=result_label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД СДЭК")
def test_get_labels_from_parcel(app):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    result_labels_from_parcel = app.document.get_labels_from_parcel(parcel_id=parcel_id[0], order_ids=order_in_parcel)
    Checking.check_status_code(response=result_labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП СД СДЭК")
def test_get_app(app, token):
    result_app = app.document.get_app()
    Checking.check_status_code(response=result_app, expected_status_code=200)


@allure.description("Получение документов СД СДЭК")
def test_get_documents(app, token):
    result_documents = app.document.get_documents()
    Checking.check_status_code(response=result_documents, expected_status_code=200)


@allure.description("Редактирование партииСД СДЭК (Удаление заказа)")
def test_remove_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    old_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    result_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    result_parcel_remove = app.parcel.patch_parcel(order_id=choice(result_order_in_parcel),
                                                   parcel_id=parcel_id[0], op="remove")
    new_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    Checking.check_status_code(response=result_parcel_remove, expected_status_code=200)
    Checking.checking_difference_len_lists(old_list=old_list_order, new_list=new_list_order)
