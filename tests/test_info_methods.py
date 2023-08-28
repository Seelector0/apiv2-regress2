from utils.global_enums import INFO
from utils.checking import Checking
import allure
import pytest
import os


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
    if code == "Cdek":
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
