from fixture.application import Application
from databases.database_connections import DataBaseConnections
from databases.database_customer_api import DataBaseCustomerApi
from databases.database_tracking_api import DataBaseTrackingApi
from utils.checking import Checking
from environment import ENV_OBJECT
import pytest
import uuid


fixture = None


@pytest.fixture(scope="module")
def app():
    """Фикстура для открытия сессии по Api"""
    global fixture
    data = {
        "grant_type": "client_credentials",
        "client_id": f"{ENV_OBJECT.client_id()}",
        "client_secret": f"{ENV_OBJECT.client_secret()}"
    }
    if fixture is None:
        fixture = Application(base_url=f"{ENV_OBJECT.get_base_url()}{'/auth/access_token'}")
    fixture.open_session(data=data, headers=fixture.headers)
    Checking.check_status_code(response=fixture.response, expected_status_code=200)
    return fixture


@pytest.fixture(scope="function")
def token():
    """Фикстура для получения токена для работы по Api"""
    fixture.token = {
        "x-trace-id": str(uuid.uuid4()),
        "Authorization": f"Bearer {fixture.response.json()['access_token']}",
        "Content-Type": "application/json"
    }
    return fixture.token


@pytest.fixture(scope="module")
def customer_api(request):
    """Фикстура для подключения к базе данных 'customer-api'"""
    database_customer = DataBaseCustomerApi(host=ENV_OBJECT.host(), database=ENV_OBJECT.db_customer_api(),
                                            user=ENV_OBJECT.db_connections(), password=ENV_OBJECT.password())

    def fin():
        database_customer.connection_close()
    request.addfinalizer(finalizer=fin)
    return database_customer


@pytest.fixture(scope="module")
def connections(request):
    """Фикстура для подключения к базе данных 'connections' для dev stage или 'metaship для local stage'"""
    database_connections = DataBaseConnections(host=ENV_OBJECT.host(), database=ENV_OBJECT.db_connections(),
                                               user=ENV_OBJECT.db_connections(), password=ENV_OBJECT.password())

    def fin():
        database_connections.connection_close()
    request.addfinalizer(finalizer=fin)
    return database_connections


@pytest.fixture(scope="module")
def tracking_api(request):
    """Фикстура для подключения к базе данных 'tracking-api'"""
    database_tracking = DataBaseTrackingApi(host=ENV_OBJECT.host(), database=ENV_OBJECT.db_tracking_api(),
                                            user=ENV_OBJECT.db_connections(), password=ENV_OBJECT.password())

    def fin():
        database_tracking.connection_close()
    request.addfinalizer(finalizer=fin)
    return database_tracking


@pytest.fixture(scope="module", autouse=True)
def stop(app, request, connections, customer_api, tracking_api):
    """Фикстура для завершения сессии"""
    def fin():
        app.close_session()
        shops = connections.get_shops_list()
        for i in shops:
            customer_api.delete_connection(shop_id=i.shop_id)
        orders = connections.get_orders_list()
        for i in orders:
            tracking_api.delete_orders_list_in_tracking(order_id=i.order_id)
        connections.delete_all_setting()
    request.addfinalizer(finalizer=fin)
