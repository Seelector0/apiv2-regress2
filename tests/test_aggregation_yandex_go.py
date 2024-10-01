import allure
import pytest
from utils.environment import ENV_OBJECT
from utils.common_tests import CommonConnections, CommonOrders, CommonParcels


@allure.description("Подключение настроек службы доставки СД YandexGo")
def test_aggregation_delivery_services(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          connection_settings=app.settings.yandex_go(aggregation=True),
                                                          moderation_settings=admin.moderation.yandex_go)


@allure.description("Создание Courier заказа по CД YandexGo")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
@pytest.mark.parametrize("execution_number", range(2))
def test_create_single_order(app, shop_id, warehouse_id, execution_number, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type="Paid", delivery_type="Courier", service="YandexGo",
                                          declared_value=0, delivery_sum=0, shared_data=shared_data["order_ids"])


@allure.description("Получение списка заказов CД YandexGo")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_get_orders(app, shared_data):
    CommonOrders.test_get_orders_common(app=app, shared_data=shared_data)


@allure.description("Получение информации о заказе CД YandexGo")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД YandexGo")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе СД YandexGo")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии СД YandexGo")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение списка партий CД YandexGo")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_get_parcels(app, shared_data):
    CommonParcels.test_get_parcels_common(app=app, shared_data=shared_data)


@allure.description("Получение информации о партии CД YandexGo")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП СД YandexGo")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД YandexGo")
@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)
