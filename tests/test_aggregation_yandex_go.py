from utils.checking import Checking
from utils.global_enums import INFO
from environment import ENV_OBJECT
import allure
import pytest


@allure.description("Создание магазина")
def test_create_shop(app, connections):
    new_shop = app.shop.post_shop()
    Checking.check_status_code(response=new_shop, expected_status_code=201)
    Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_shops_value(shop_id=new_shop.json()["id"], value="deleted"),
        two_value=[False])
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_shops_value(shop_id=new_shop.json()["id"], value="visibility"),
        two_value=[True])


@allure.description("Создание склада")
def test_create_warehouse(app, connections):
    new_warehouse = app.warehouse.post_warehouse()
    Checking.check_status_code(response=new_warehouse, expected_status_code=201)
    Checking.checking_json_key(response=new_warehouse, expected_value=INFO.created_entity)
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_warehouses_value(warehouse_id=new_warehouse.json()["id"],
                                                                 value="deleted"),
        two_value=[False])
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_warehouses_value(warehouse_id=new_warehouse.json()["id"],
                                                                 value="visibility"),
        two_value=[True])


@allure.description("Подключение настроек СД YandexGo по агрегации")
def test_aggregation_delivery_services(app):
    yandex = app.service.delivery_services_yandex_go(aggregation=True)
    Checking.check_status_code(response=yandex, expected_status_code=201)
    Checking.checking_json_key(response=yandex, expected_value=INFO.created_entity)


@allure.description("Модерация СД YandexGo")
def test_moderation_delivery_services(admin):
    moderation = admin.moderation.moderation_yandex_go()
    Checking.check_status_code(response=moderation, expected_status_code=200)
    Checking.checking_json_key(response=moderation, expected_value=INFO.entity_moderation)


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
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
@pytest.mark.parametrize("execution_number", range(2))
def test_create_order_courier(app, execution_number, connections):
    new_order = app.order.post_single_order(payment_type="Paid", type_ds="Courier", service="YandexGo",
                                            declared_value=0, delivery_sum=0)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Получение информации об истории изменения статусов заказа СД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
def test_order_status(app, connections):
    for order_id in connections.metaship.get_list_all_orders():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе СД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
def test_order_details(app, connections):
    for order_id in connections.metaship.get_list_all_orders():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии СД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
def test_create_parcel(app, connections):
    orders_id = connections.metaship.get_list_all_orders()
    create_parcel = app.parcel.post_parcel(all_orders=True, order_id=orders_id)
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение АПП СД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов СД YandexGo")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)
