from utils.checking import Checking
from utils.enums.global_enums import OtherInfo
from random import choice
import pytest
import allure


# Todo когда будут моки, добавлю метод patch для многоместных заказов


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


@allure.description("Подключение настроек СД DostavkaClub")
def test_integration_delivery_services(app, token):
    result_dostavka_club = app.service.delivery_services_dostavka_club()
    Checking.check_status_code(response=result_dostavka_club, expected_status_code=201)
    Checking.checking_json_key(response=result_dostavka_club, expected_value=["id", "type", "url", "status"])
    result_get_dostavka_club = app.service.get_delivery_services_code(code="DostavkaClub")
    Checking.check_status_code(response=result_get_dostavka_club, expected_status_code=200)
    Checking.checking_json_value(response=result_get_dostavka_club, key_name="code", expected_value="DostavkaClub")
    Checking.checking_json_value(response=result_get_dostavka_club, key_name="credentials", field="visibility",
                                 expected_value=True)


@allure.description("Получения сроков доставки по DostavkaClub")
def test_delivery_time_schedules(app, token):
    result_delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="DostavkaClub")
    Checking.check_status_code(response=result_delivery_time_schedules, expected_status_code=200)
    Checking.checking_json_value(response=result_delivery_time_schedules, key_name="intervals",
                                 expected_value=OtherInfo.CLUB_INTERVALS.value)


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД DostavkaClub")
def test_info_vats(app, token):
    result_info_vats = app.info.info_vats(delivery_service_code="DostavkaClub")
    Checking.check_status_code(response=result_info_vats, expected_status_code=200)
    Checking.checking_json_key(response=result_info_vats, expected_value=OtherInfo.CLUB_VATS.value)


@allure.description("Получение актуального списка возможных статусов заказа СД DostavkaClub")
def test_info_statuses(app, token):
    result_info_delivery_service_services = app.info.info_delivery_service_services(code="DostavkaClub")
    Checking.check_status_code(response=result_info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=result_info_delivery_service_services,
                               expected_value=OtherInfo.CLUB_SERVICES.value)


@allure.description("Получение оферов по DostavkaClub (Courier)")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type, token):
    result_offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier",
                                                  delivery_service_code="DostavkaClub")
    Checking.check_status_code(response=result_offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=result_offers_courier, expected_value=["Courier"])


@allure.description("Создание Courier многоместного заказа по CД DostavkaClub")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, token, payment_type):
    result_multi_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier",
                                                    service="DostavkaClub",
                                                    tariff=choice(OtherInfo.CLUB_TARIFFS.value), declared_value=1500)
    Checking.check_status_code(response=result_multi_order, expected_status_code=201)
    Checking.checking_json_key(response=result_multi_order, expected_value=["id", "type", "url", "status"])
    result_get_order_by_id = app.order.get_order_id(order_id=result_multi_order.json()["id"], sec=5)
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Создание Courier заказа по CД DostavkaClub")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, token, payment_type):
    result_order = app.order.post_order(payment_type=payment_type, type_ds="Courier", service="DostavkaClub",
                                        tariff=choice(OtherInfo.CLUB_TARIFFS.value), price=1000, declared_value=1500)
    Checking.check_status_code(response=result_order, expected_status_code=201)
    Checking.checking_json_key(response=result_order, expected_value=["id", "type", "url", "status"])
    result_get_order_by_id = app.order.get_order_id(order_id=result_order.json()["id"], sec=5)
    Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Получение информации об истории изменения статусов заказа СД DostavkaClub")
def test_order_status(app, token):
    order_list_id = app.order.getting_order_id_out_parcel()
    for order_id in order_list_id:
        result_order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=result_order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=result_order_status, key_name="status", expected_value="created")


@allure.description("Попытка получения этикетки DostavkaClub")
def test_get_label_out_of_parcel(app, token):
    list_order_id = app.order.getting_order_id_out_parcel()
    for order_id in list_order_id:
        result_label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=result_label, expected_status_code=404)


@allure.description("Попытка редактирования заказа СД DostavkaClub")
def test_editing_order(app, token):
    order_list_id = app.order.getting_order_id_out_parcel()
    result_order_put = app.order.put_order(order_id=choice(order_list_id), weight=5, length=12, width=14, height=11,
                                           declared_value=2500, family_name="Иванов")
    Checking.check_status_code(response=result_order_put, expected_status_code=400)


@allure.description("Получение подробной информации о заказе CД DostavkaClub")
def test_order_details(app, token):
    order_list_id = app.order.getting_order_id_out_parcel()
    for order_id in order_list_id:
        result_order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=result_order_details, expected_status_code=200)
        Checking.checking_json_key(response=result_order_details, expected_value=OtherInfo.DETAILS.value)


@allure.description("Создание партии CД DostavkaClub")
def test_create_parcel(app, token):
    orders_id = app.order.getting_order_id_out_parcel()
    result_create_parcel = app.parcel.post_parcel(all_orders=True, order_id=orders_id)
    Checking.check_status_code(response=result_create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=result_create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Редактирование партии CД DostavkaClub (Попытка изменения даты отправки партии)")
def test_change_shipment_date(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    result_shipment_date = app.parcel.patch_parcel_shipment_date(parcel_id=parcel_id[0], day=5)
    Checking.check_status_code(response=result_shipment_date, expected_status_code=422)


@allure.description("Получение АПП CД DostavkaClub")
def test_get_app(app, token):
    result_app = app.document.get_acceptance()
    Checking.check_status_code(response=result_app, expected_status_code=200)


@allure.description("Получение документов CД DostavkaClub")
def test_get_documents(app, token):
    result_documents = app.document.get_files()
    Checking.check_status_code(response=result_documents, expected_status_code=200)


@allure.description("Попытка Редактирование партии CД DostavkaClub (Удаление заказа)")
def test_remove_order_in_parcel(app, token):
    parcel_id = app.parcel.getting_list_of_parcels_ids()
    result_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
    result_parcel_remove = app.parcel.patch_parcel(order_id=choice(result_order_in_parcel), parcel_id=parcel_id[0],
                                                   op="remove")
    Checking.check_status_code(response=result_parcel_remove, expected_status_code=422)
