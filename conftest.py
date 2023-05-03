from fixture.application import Application
from databases.database_connections import DataBaseConnections
from databases.database_customer_api import DataBaseCustomerApi
from databases.database_tracking_api import DataBaseTrackingApi
from utils.checking import Checking
from environment import ENV_OBJECT
import pytest
import uuid


fixture_api = None
fixture_database = None


@pytest.fixture(scope="module")
def app():
    """Фикстура для открытия сессии по Api"""
    global fixture_api
    if fixture_api is None:
        fixture_api = Application(base_url=f"{ENV_OBJECT.get_base_url()}/auth/access_token")
    fixture_api.open_session()
    Checking.check_status_code(response=fixture_api.response, expected_status_code=200)
    return fixture_api


@pytest.fixture(scope="function")
def token():
    """Фикстура для получения токена для работы по Api"""
    fixture_api.token = {
        "x-trace-id": str(uuid.uuid4()),
        "Authorization": f"Bearer {fixture_api.response.json()['access_token']}"
    }
    return fixture_api.token


@pytest.fixture(scope="module")
def customer_api():
    """Фикстура для подключения к базе данных 'customer-api'"""
    database_customer = DataBaseCustomerApi(host=ENV_OBJECT.host(), database=ENV_OBJECT.db_customer_api(),
                                            user=ENV_OBJECT.db_connections(), password=ENV_OBJECT.password())
    database_customer.connection_open()
    return database_customer


@pytest.fixture(scope="module")
def connections():
    """Фикстура для подключения к базе данных 'connections' для dev stage или 'metaship для local stage'"""
    global fixture_database
    if fixture_database is None:
        fixture_database = DataBaseConnections(host=ENV_OBJECT.host(), database=ENV_OBJECT.db_connections(),
                                               user=ENV_OBJECT.db_connections(), password=ENV_OBJECT.password())
    fixture_database.connection_open()
    return fixture_database


@pytest.fixture(scope="module")
def tracking_api():
    """Фикстура для подключения к базе данных 'tracking-api'"""
    database_tracking = DataBaseTrackingApi(host=ENV_OBJECT.host(), database=ENV_OBJECT.db_tracking_api(),
                                            user=ENV_OBJECT.db_connections(), password=ENV_OBJECT.password())
    database_tracking.connection_open()
    return database_tracking


@pytest.fixture(scope="module", autouse=True)
def stop(app, request, connections, customer_api, tracking_api):
    """Фикстура для завершения сессии"""
    def fin():
        app.close_session()
        for i in connections.get_shops_list():
            customer_api.delete_connection(shop_id=i.shop_id)
        for i in connections.get_orders_list():
            tracking_api.delete_orders_list_in_tracking(order_id=i.order_id)
        connections.delete_all_setting()
        connections.connection_close()
        customer_api.connection_close()
        tracking_api.connection_close()
    request.addfinalizer(finalizer=fin)
