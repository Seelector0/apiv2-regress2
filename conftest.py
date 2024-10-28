from databases.connections import DataBaseConnections
from databases.customer_api import DataBaseCustomerApi
from databases.tracking_api import DataBaseTrackingApi
from databases.widget_api import DataBaseWidgetApi
from utils.helper.test_warehouses import TestsWarehouse
from fixture.application import Application
from fixture.admin import Admin
import pytest
import logging


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", force=True)


@pytest.fixture(scope="module")
def app(connections):
    """Фикстура для открытия сессии по Apiv2 metaship."""
    apiv2 = Application(connections=connections)
    apiv2.authorization.post_access_token()
    yield apiv2
    apiv2.authorization.session.close()


@pytest.fixture(scope="module")
def admin(customer_api):
    """Фикстура для открытия сессии по Admin Api."""
    api_admin = Admin(customer_api=customer_api)
    api_admin.authorization.post_access_token(admin=True)
    yield api_admin
    api_admin.authorization.session.close()


@pytest.fixture(scope="module")
def connections():
    """Фикстура для подключения к базе данных 'connections' для dev stage или 'metaship для local stage'."""
    db_connections = DataBaseConnections()
    yield db_connections
    db_connections.close_connection()


@pytest.fixture(scope="module")
def customer_api():
    """Фикстура для подключения к базе данных 'customer-api'"""
    db_customer_api = DataBaseCustomerApi()
    yield db_customer_api
    db_customer_api.close_connection()


@pytest.fixture(scope="module")
def tracking_api():
    """Фикстура для подключения к базе данных 'tracking-api'"""
    return DataBaseTrackingApi()


@pytest.fixture(scope="module")
def widget_api():
    """Фикстура для подключения к базе данных 'widget-api'"""
    return DataBaseWidgetApi()


@pytest.fixture(scope="module", autouse=True)
def stop(request, connections, shared_data):
    """Фикстура для очистки данных после тестов."""

    def fin():
        try:
            for id_ in [shared_data["shop_id"], shared_data["shop_id_metaship"]]:
                if id_:
                    connections.delete_list_orders_for_shop(shop_id=id_)
                    connections.delete_list_shops_for_id(shop_id=id_)
            for id_ in [shared_data["warehouse_id"], shared_data["warehouse_without_pickup"],
                        shared_data["warehouse_id_kz"]]:
                if id_:
                    connections.delete_list_warehouses_for_id(warehouse_id=id_)
            for service_data in shared_data.values():
                if isinstance(service_data, dict) and "parcel_ids" in service_data:
                    for parcel_id in service_data["parcel_ids"]:
                        connections.delete_list_parcels_for_id(parcel_id)
                        connections.delete_order_parcel(parcel_id)
        except Exception as e:
            print(f"Ошибка при очистке данных: {e}")

    request.addfinalizer(finalizer=fin)


@pytest.fixture(scope="module")
def shared_data():
    """Фикстура для хранения тестовых данных"""

    def delivery_service_template():
        return {"order_ids": [], "order_ids_single": [], "parcel_ids": [], "order_ids_in_parcel": []}

    def russian_post_template():
        return {"order_ids": [], "orders_courier": [], "orders_post_office": [], "orders_delivery_point": [],
                "orders_terminal": [], "parcel_ids": [], "parcel_ids_courier": [], "order_ids_in_parcel": [],
                "parcel_ids_post_office": [], "parcel_ids_delivery_point": [], "parcel_ids_terminal": []}

    data = {
        "alemtat_a": delivery_service_template(),
        "alemtat_i": delivery_service_template(),
        "boxberry_a": delivery_service_template(),
        "boxberry_i": delivery_service_template(),
        "cdek_a": delivery_service_template(),
        "cdek_i": delivery_service_template(),
        "cse_a": delivery_service_template(),
        "cse_i": delivery_service_template(),
        "dalli_a": delivery_service_template(),
        "dalli_i": delivery_service_template(),
        "dpd_a": delivery_service_template(),
        "dpd_i": delivery_service_template(),
        "halva_a": delivery_service_template(),
        "halva_i": delivery_service_template(),
        "l_post_i": delivery_service_template(),
        "metaship_a": delivery_service_template(),
        "kaz_post_a": delivery_service_template(),
        "kaz_post_i": delivery_service_template(),
        "five_post_a": delivery_service_template(),
        "five_post_i": delivery_service_template(),
        "russian_post_a": russian_post_template(),
        "russian_post_i": russian_post_template(),
        "top_delivery_a": delivery_service_template(),
        "top_delivery_i": delivery_service_template(),
        "pecom_a": delivery_service_template(),
        "pecom_i": delivery_service_template(),
        "pony_express_a": delivery_service_template(),
        "pony_express_i": delivery_service_template(),
        "yandex_delivery_a": delivery_service_template(),
        "yandex_delivery_i": delivery_service_template(),
        "yandex_go_a": delivery_service_template(),
        "yandex_go_i": delivery_service_template(),

        "shop_id": None,
        "shop_id_metaship": None,
        "warehouse_id": None,
        "warehouse_without_pickup": None,
        "warehouse_id_kz": None
    }
    return data


@pytest.fixture(scope='module')
def warehouse_id(app, connections, shared_data):
    """Фикстура создания склада"""
    tests_warehouse = TestsWarehouse(app, connections)
    warehouse_id = tests_warehouse.post_warehouse(pickup=True)
    shared_data["warehouse_id"] = warehouse_id
    return warehouse_id


@pytest.fixture(scope='module')
def warehouse_without_pickup(app, connections, shared_data):
    """Фикстура создания склада"""
    tests_warehouse = TestsWarehouse(app, connections)
    warehouse_without_pickup = tests_warehouse.post_warehouse(pickup=False)
    shared_data["warehouse_without_pickup"] = warehouse_without_pickup
    return warehouse_without_pickup


@pytest.fixture(scope='module')
def warehouse_id_kz(app, connections, shared_data):
    """Фикстура создания склада для Казахстана"""
    tests_warehouse = TestsWarehouse(app, connections)
    warehouse_id_kz = tests_warehouse.post_warehouse(country_code="KZ", pickup=True)
    shared_data["warehouse_id_kz"] = warehouse_id_kz
    return warehouse_id_kz
