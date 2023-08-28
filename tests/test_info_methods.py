from utils.global_enums import INFO
from utils.checking import Checking
import allure
import pytest
import os


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать конкретная СД")
@pytest.mark.parametrize("delivery_service_code", ["Boxberry", "Cdek", "Cse", "Dalli", "DostavkaClub", "DostavkaGuru",
                                                   "Dpd", "FivePost", "LPost", "RussianPost", "TopDelivery", "YandexGo",
                                                   "YandexDelivery"])
def test_info_vats(app, delivery_service_code):
    info_vats = app.info.info_vats(delivery_service_code=delivery_service_code)
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    if delivery_service_code == "Boxberry":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.boxberry_vats)
    elif delivery_service_code == "Cdek":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.cdek_vats)
    elif delivery_service_code == "Cse":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.cse_vats)
    elif delivery_service_code == "Dalli":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.dalli_vats)
    elif delivery_service_code == "DostavkaClub":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.club_vats)
    elif delivery_service_code == "DostavkaGuru":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.guru_vats)
    elif delivery_service_code == "Dpd":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.dpd_vats)
    elif delivery_service_code == "FivePost":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.five_post_vats)
    elif delivery_service_code == "LPost":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.l_post_vats)
    elif delivery_service_code == "RussianPost":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.rp_vats)
    elif delivery_service_code == "TopDelivery":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.topdelivery_vats)
    elif delivery_service_code == "YandexGo":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.yandex_go_vats)
    elif delivery_service_code == "YandexDelivery":
        Checking.checking_json_key(response=info_vats, expected_value=INFO.yandex_delivery_vats)


@allure.description("Получение списка точек сдачи СД")
@pytest.mark.parametrize("delivery_service_code", ["Boxberry", "Cdek", "Dpd", "RussianPost", "YandexDelivery"])
def test_intake_offices(app, delivery_service_code):
    intake_offices = app.info.intake_offices(delivery_service_code=delivery_service_code)
    Checking.check_status_code(response=intake_offices, expected_status_code=200)
    Checking.check_response_is_not_empty(response=intake_offices)
    Checking.checking_in_list_json_value(response=intake_offices, key_name="deliveryServiceCode",
                                         expected_value=delivery_service_code)


@allure.description("Получение полного актуального списка возможных статусов заказа")
def test_info_order_statuses(app):
    order_statuses = app.info.info_statuses()
    Checking.check_status_code(response=order_statuses, expected_status_code=200)
    Checking.checking_json_key(response=order_statuses, expected_value=INFO.entity_order_statuses)


@allure.description("Получение информации о тарифах поддерживаемых СД")
@pytest.mark.parametrize("code", ["RussianPost", "Cdek"])
def tests_tariffs(app, code):
    list_tariffs = app.info.get_tariffs(code=code)
    Checking.check_status_code(response=list_tariffs, expected_status_code=200)
    if code == "RussianPost":
        Checking.checking_json_key(response=list_tariffs, expected_value=INFO.rp_list_tariffs)
    elif code == "Cdek":
        Checking.checking_json_key(response=list_tariffs, expected_value=INFO.cdek_list_tariffs)


@allure.description("Получение списка ключей")
def test_user_clients(app):
    user_clients = app.info.user_clients()
    Checking.check_status_code(response=user_clients, expected_status_code=200)
    for user in user_clients.json():
        Checking.check_value_comparison(one_value=user["name"], two_value="Клиент APIv2")
        Checking.check_value_comparison(one_value=user["active"], two_value=True)


@allure.description("Получение информации о ключе подключения")
def test_user_clients_by_id(app, connections):
    if connections.db_connections == "metaship":
        clients_id = app.info.user_clients_id(user_id=os.getenv("CLIENT_ID_LOCAL"))
        Checking.check_status_code(response=clients_id, expected_status_code=200)
        Checking.checking_json_value(response=clients_id, key_name="id", expected_value=os.getenv("CLIENT_ID_LOCAL"))
        Checking.checking_json_value(response=clients_id, key_name="secret",
                                     expected_value=os.getenv("CLIENT_SECRET_LOCAL"))
    else:
        clients_id = app.info.user_clients_id(user_id=os.getenv("CLIENT_ID"))
        Checking.check_status_code(response=clients_id, expected_status_code=200)
        Checking.checking_json_value(response=clients_id, key_name="id", expected_value=os.getenv("CLIENT_ID"))
        Checking.checking_json_value(response=clients_id, key_name="secret", expected_value=os.getenv("CLIENT_SECRET"))


@allure.description("Разбор адреса")
def test_address(app):
    address = app.info.info_address(raw="119633 г Москва Боровское шоссе 33")
    Checking.check_status_code(response=address, expected_status_code=200)
    Checking.checking_json_value(response=address, key_name="raw",
                                 expected_value="119633, г Москва, р-н Ново-Переделкино, Боровское шоссе, д 33")
    Checking.checking_json_value(response=address, key_name="postCode", expected_value="119633")
