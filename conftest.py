from fixture.application import Application
from fixture.database import DataBase
from environment import ENV_OBJECT
import pytest


fixture_api = None
fixture_connections = None
fixture_customer = None
fixture_tracking = None


@pytest.fixture(scope="module")
def app():
    """Фикстура для открытия сессии по Api"""
    global fixture_api
    if fixture_api is None:
        fixture_api = Application(base_url=f"{ENV_OBJECT.get_base_url()}/auth/access_token")
    fixture_api.open_session()
    return fixture_api


@pytest.fixture(scope="module")
def connections():
    """Фикстура для подключения к базе данных 'connections' для dev stage или 'metaship для local stage'"""
    global fixture_connections
    if fixture_connections is None:
        fixture_connections = DataBase(database=ENV_OBJECT.db_connections())
    fixture_connections.connection_open()
    return fixture_connections


@pytest.fixture(scope="module")
def customer_api():
    """Фикстура для подключения к базе данных 'customer-api'"""
    global fixture_customer
    if fixture_customer is None:
        fixture_customer = DataBase(database=ENV_OBJECT.db_customer_api())
    fixture_customer.connection_open()
    return fixture_customer


@pytest.fixture(scope="module")
def tracking_api():
    """Фикстура для подключения к базе данных 'tracking-api'"""
    global fixture_tracking
    if fixture_tracking is None:
        fixture_tracking = DataBase(database=ENV_OBJECT.db_tracking_api())
    fixture_tracking.connection_open()
    return fixture_tracking


@pytest.fixture(scope="module", autouse=True)
def stop(app, request, connections, customer_api, tracking_api):
    """Фикстура для завершения сессии"""
    def fin():
        app.close_session()
        for id_ in connections.metaship.get_list_shops():
            customer_api.customer.delete_connection(shop_id=id_)
        for id_ in connections.metaship.get_list_orders():
            tracking_api.tracking.delete_list_orders_in_tracking(order_id=id_)
        connections.metaship.delete_all_setting()
        connections.connection_close()
        customer_api.connection_close()
        tracking_api.connection_close()
    request.addfinalizer(finalizer=fin)
