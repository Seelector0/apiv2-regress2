import allure
import pytest
import os
from utils.common_tests import CommonInfo
from utils.dates import tomorrow
from utils.environment import ENV_OBJECT
from utils.global_enums import INFO
from utils.checking import Checking


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать конкретная СД")
@pytest.mark.parametrize("delivery_service_code", ["Boxberry", "Cdek", "Cse", "Dalli", "DostavkaClub", "Dpd",
                                                   "FivePost", "LPost", "RussianPost", "TopDelivery", "YandexGo",
                                                   "YandexDelivery", "Halva", "Pecom"])
def test_info_vats(app, delivery_service_code):
    info_vats = app.info.get_info_vats(delivery_service_code=delivery_service_code)
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    if delivery_service_code == "Boxberry":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.boxberry_vats)
    elif delivery_service_code == "Cdek":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.cdek_vats)
    elif delivery_service_code == "Cse":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.cse_vats)
    elif delivery_service_code == "Dalli":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.dalli_vats)
    elif delivery_service_code == "DostavkaClub":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.club_vats)
    elif delivery_service_code == "Dpd":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.dpd_vats)
    elif delivery_service_code == "FivePost":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.five_post_vats)
    elif delivery_service_code == "LPost":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.l_post_vats)
    elif delivery_service_code == "RussianPost":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.rp_vats)
    elif delivery_service_code == "TopDelivery":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.topdelivery_vats)
    elif delivery_service_code == "YandexGo":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.ya_go_vats)
    elif delivery_service_code == "YandexDelivery":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.ya_delivery_vats)
    elif delivery_service_code == "Halva":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.halva_vats)
    elif delivery_service_code == "Pecom":
        Checking.checking_json_contains(response=info_vats, expected_values=INFO.pecom_vats)


@allure.description("Получение списка точек сдачи СД")
@pytest.mark.parametrize("delivery_service_code", ["Boxberry", "Cdek", "Dpd", "RussianPost", "YandexDelivery"])
def test_intake_offices(app, delivery_service_code):
    intake_offices = app.info.get_intake_offices(delivery_service_code=delivery_service_code)
    Checking.check_status_code(response=intake_offices, expected_status_code=200)
    Checking.check_response_is_not_empty(response=intake_offices)
    Checking.checking_in_list_json_value(response=intake_offices, key_name="deliveryServiceCode",
                                         expected_value=delivery_service_code)


@allure.description("Получение информации о тарифах поддерживаемых СД")
@pytest.mark.parametrize("code", ["RussianPost", "Cdek"])
def tests_tariffs(app, code):
    list_tariffs = app.info.get_tariffs(code=code)
    Checking.check_status_code(response=list_tariffs, expected_status_code=200)
    if code == "RussianPost":
        Checking.checking_json_contains(response=list_tariffs, expected_values=INFO.rp_list_tariffs)
    elif code == "Cdek":
        Checking.checking_json_contains(response=list_tariffs, expected_values=INFO.cdek_list_tariffs)


@allure.description("Получение информации о дополнительных услугах поддерживаемых СД")
@pytest.mark.parametrize("delivery_service_code", ["Boxberry", "Cdek", "Cse", "Dalli", "DostavkaClub", "Dpd",
                                                   "FivePost", "LPost", "RussianPost", "TopDelivery", "YandexGo",
                                                   "YandexDelivery", "Pecom", "KazPost"])
def test_info_statuses(app, delivery_service_code):
    info_delivery_service_services = app.info.get_info_delivery_service_services(code=delivery_service_code)
    Checking.check_status_code(response=info_delivery_service_services, expected_status_code=200)
    if delivery_service_code == "Boxberry":
        Checking.checking_json_contains(response=info_delivery_service_services, expected_values=INFO.boxberry_services)
    elif delivery_service_code == "Cdek":
        Checking.checking_json_contains(response=info_delivery_service_services, expected_values=INFO.cdek_services)
    elif delivery_service_code == "Cse":
        Checking.checking_json_contains(response=info_delivery_service_services, expected_values=INFO.cse_services)
    elif delivery_service_code == "Dalli":
        Checking.checking_json_contains(response=info_delivery_service_services, expected_values=INFO.dalli_services)
    elif delivery_service_code == "DostavkaClub":
        Checking.checking_json_contains(response=info_delivery_service_services, expected_values=INFO.club_services)
    elif delivery_service_code == "Dpd":
        Checking.checking_json_contains(response=info_delivery_service_services, expected_values=INFO.dpd_services)
    elif delivery_service_code == "FivePost":
        Checking.checking_json_contains(response=info_delivery_service_services,
                                        expected_values=INFO.five_post_services)
    elif delivery_service_code == "LPost":
        Checking.checking_json_contains(response=info_delivery_service_services, expected_values=INFO.l_post_services)
    elif delivery_service_code == "RussianPost":
        Checking.checking_json_contains(response=info_delivery_service_services, expected_values=INFO.rp_services)
    elif delivery_service_code == "TopDelivery":
        Checking.checking_json_contains(response=info_delivery_service_services,
                                        expected_values=INFO.topdelivery_services)
    elif delivery_service_code == "YandexGo":
        Checking.checking_json_contains(response=info_delivery_service_services, expected_values=INFO.ya_go_services)
    elif delivery_service_code == "YandexDelivery":
        Checking.checking_json_contains(response=info_delivery_service_services,
                                        expected_values=INFO.ya_delivery_services)
    elif delivery_service_code == "Pecom":
        Checking.checking_json_contains(response=info_delivery_service_services, expected_values=INFO.pecom_services)
    elif delivery_service_code == "KazPost":
        Checking.checking_json_contains(response=info_delivery_service_services,
                                        expected_values=INFO.ds_kazakhstan_services)
    elif delivery_service_code == "AlemTat":
        Checking.checking_json_contains(response=info_delivery_service_services,
                                        expected_values=INFO.ds_kazakhstan_services)
    elif delivery_service_code == "PonyExpress":
        Checking.checking_json_contains(response=info_delivery_service_services,
                                        expected_values=INFO.ds_kazakhstan_services)


@allure.description("Получение интервалов доставки")
@pytest.mark.parametrize("delivery_service_code, tariff_id", [("Boxberry", None), ("TopDelivery", None),
                                                              ("Dalli", "1")])
def test_delivery_time_schedules(app, shop_id, delivery_service_code, tariff_id):
    CommonInfo.test_delivery_time_schedules_common(app=app, shop_id=shop_id,
                                                   delivery_service_code=delivery_service_code, data=tomorrow,
                                                   tariff_id=tariff_id)


@allure.description("Получение списка ключей")
def test_user_clients(app):
    user_clients = app.info.get_user_clients()
    Checking.check_status_code(response=user_clients, expected_status_code=200)
    for user in user_clients.json():
        Checking.check_value_comparison(responses={"GET v2/user/clients": user_clients}, one_value=user["name"],
                                        two_value="Клиент APIv2")
        Checking.check_value_comparison(responses={"GET v2/user/clients": user_clients}, one_value=user["active"],
                                        two_value=True)


@allure.description("Получение информации о ключе подключения")
def test_user_clients_by_id(app):
    if ENV_OBJECT.db_connections() == "metaship":
        clients_id = app.info.get_user_clients_id(user_id=os.getenv("CLIENT_ID_LOCAL"))
        Checking.check_status_code(response=clients_id, expected_status_code=200)
        Checking.checking_json_value(response=clients_id, key_name="id", expected_value=os.getenv("CLIENT_ID_LOCAL"))
        Checking.checking_json_value(response=clients_id, key_name="secret",
                                     expected_value=os.getenv("CLIENT_SECRET_LOCAL"))
    else:
        clients_id = app.info.get_user_clients_id(user_id=os.getenv("CLIENT_ID"))
        Checking.check_status_code(response=clients_id, expected_status_code=200)
        Checking.checking_json_value(response=clients_id, key_name="id", expected_value=os.getenv("CLIENT_ID"))
        Checking.checking_json_value(response=clients_id, key_name="secret", expected_value=os.getenv("CLIENT_SECRET"))


@allure.description("Разбор адреса")
def test_address(app):
    address = app.info.get_info_address(raw="119633 г Москва Боровское шоссе 33")
    Checking.check_status_code(response=address, expected_status_code=200)
    Checking.checking_json_value(response=address, key_name="raw",
                                 expected_value="119633, г Москва, р-н Ново-Переделкино, Боровское шоссе, д 33")
    Checking.checking_json_value(response=address, key_name="postCode", expected_value="119633")
