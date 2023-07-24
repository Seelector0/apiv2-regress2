from utils.enums.global_enums import INFO
from utils.checking import Checking
from environment import ENV_OBJECT
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


@allure.description("Подключение настроек СД YandexGo")
def test_integration_delivery_services(app):
    yandex = app.service.delivery_services_yandex_go()
    Checking.check_status_code(response=yandex, expected_status_code=201)
    Checking.checking_json_key(response=yandex, expected_value=INFO.created_entity)
    get_yandex = app.service.get_delivery_services_code(code="YandexGo")
    Checking.check_status_code(response=get_yandex, expected_status_code=200)
    Checking.checking_json_value(response=get_yandex, key_name="code", expected_value="YandexGo")
    Checking.checking_json_value(response=get_yandex, key_name="credentials", field="visibility", expected_value=True)


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД YandexGo")
def test_info_vats(app):
    info_vats = app.info.info_vats(delivery_service_code="YandexGo")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.yandex_go_vats)


@allure.description("Получение актуального списка возможных сервисов заказа СД YandexGo")
def test_info_statuses(app):
    info_delivery_service_services = app.info.info_delivery_service_services(code="YandexGo")
    Checking.check_status_code(response=info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=info_delivery_service_services, expected_value=INFO.yandex_go_services)


@allure.description("Создание Courier заказа по CД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship",
                    reason="Тест работает только на dev стенде")
@pytest.mark.parametrize("execution_number", range(2))
def test_create_order_courier(app, execution_number, connections):
    new_order = app.order.post_order(payment_type="Paid", type_ds="Courier", service="YandexGo", declared_value=0,
                                     delivery_sum=0)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    get_order_by_id = app.order.get_order_id(order_id=new_order.json()["id"])
    Checking.check_status_code(response=get_order_by_id, expected_status_code=200)
    Checking.checking_json_value(response=get_order_by_id, key_name="status", expected_value="created")
    Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="succeeded")


@allure.description("Получение информации об истории изменения статусов заказа СД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship",
                    reason="Тест работает только на dev стенде")
def test_order_status(app):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе СД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship",
                    reason="Тест работает только на dev стенде")
def test_order_details(app):
    for order_id in app.order.getting_all_order_id_out_parcel():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship",
                    reason="Тест работает только на dev стенде")
def test_create_parcel(app):
    orders_id = app.order.getting_all_order_id_out_parcel()
    create_parcel = app.parcel.post_parcel(all_orders=True, order_id=orders_id)
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение АПП СД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship",
                    reason="Тест работает только на dev стенде")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship",
                    reason="Тест работает только на dev стенде")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)
