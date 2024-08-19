from databases.connections import DataBaseConnections
from databases.customer_api import DataBaseCustomerApi
from databases.tracking_api import DataBaseTrackingApi
from databases.widget_api import DataBaseWidgetApi
from utils.environment import ENV_OBJECT
from utils.helper.test_shops import TestsShop
from utils.helper.test_warehouses import TestsWarehouse
from fixture.application import Application
from fixture.admin import Admin
import time
import pytest
import requests


def check_api_availability():
    """Функция для проверки доступности API с ограниченным количеством попыток и интервалом между запросами."""
    start_time = time.time()
    timeout = 60
    response = None
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            break
        try:
            response = requests.get(url=f"{ENV_OBJECT.get_base_url()}/health/check")
            if response.status_code == 200:
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(5)

    pytest.fail(f"API не доступно по истечению {timeout} секунд. Статус-код ответа: {response.status_code}")

def pytest_sessionstart(session):
    """Хук для выполнения проверки, только в главном процессе (мастере)."""
    if not hasattr(session.config, "workerinput"):
        check_api_availability()


@pytest.fixture(scope="module")
def app(connections):
    """Фикстура для открытия сессии по Apiv2 metaship."""
    apiv2 = Application(connections=connections)
    apiv2.authorization.post_access_token()
    return apiv2


@pytest.fixture(scope="module")
def admin(customer_api):
    """Фикстура для открытия сессии по Admin Api."""
    api_admin = Admin(customer_api=customer_api)
    api_admin.authorization.post_access_token(admin=True)
    return api_admin


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
def stop(request, admin, app, connections, shop_id, shared_data):
    """Фикстура для завершения сессии"""

    def fin():
        admin.authorization.session.close()
        app.authorization.session.close()
        connections.delete_list_orders_for_shop(shop_id=shop_id)
        for id_ in shared_data["parcel_ids"]:
            connections.delete_list_parcels_for_id(id_)
            connections.delete_order_parcel(id_)

    request.addfinalizer(finalizer=fin)


@pytest.fixture(scope="module")
def shared_data():
    """Фикстура для хранения тестовых данных"""
    data = {
        "order_ids": [],
        "order_ids_single": [],
        "orders_courier": [],
        "orders_post_office": [],
        "orders_delivery_point": [],
        "orders_terminal": [],
        "order_ids_in_parcel": [],
        "parcel_ids": [],
        "parcel_ids_courier": [],
        "parcel_ids_post_office": [],
        "parcel_ids_delivery_point": [],
        "parcel_ids_terminal": []
    }
    return data


@pytest.fixture(scope='module')
def shop_id(app, connections):
    """Фикстура создания магазина"""
    tests_shop = TestsShop(app, connections)
    shop_id = tests_shop.post_shop()
    return shop_id


@pytest.fixture(scope='module')
def shop_id_metaship(app, connections):
    """Фикстура создания магазина для сд меташип"""
    tests_shop = TestsShop(app, connections)
    shop_id_metaship = tests_shop.post_shop()
    return shop_id_metaship


@pytest.fixture(scope='module')
def warehouse_id(app, connections):
    """Фикстура создания склада"""
    tests_warehouse = TestsWarehouse(app, connections)
    warehouse_id = tests_warehouse.post_warehouse()
    return warehouse_id


@pytest.fixture(scope='module')
def warehouse_id_kz(app, connections):
    """Фикстура создания склада для Казахстана"""
    tests_warehouse = TestsWarehouse(app, connections)
    warehouse_id_kz = tests_warehouse.post_warehouse(country_code="KZ")
    return warehouse_id_kz
