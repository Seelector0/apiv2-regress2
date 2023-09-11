from databases.connections import DataBaseConnections
from databases.customer_api import DataBaseCustomerApi
from databases.tracking_api import DataBaseTrackingApi
from databases.widget_api import DataBaseWidgetApi
from fixture.application import Application
from environment import ENV_OBJECT
from fixture.admin import Admin
import pytest


url = f"{ENV_OBJECT.get_base_url()}/auth/access_token"


@pytest.fixture(scope="module")
def app():
    """Фикстура для открытия сессии по Apiv2 metaship."""
    apiv2_metaship = Application(base_url=url)
    apiv2_metaship.open_session()
    return apiv2_metaship


@pytest.fixture(scope="function")
def admin():
    """Фикстура для открытия сессии по Admin Api."""
    api_admin = Admin(base_url=url)
    api_admin.admin_session()
    return api_admin


@pytest.fixture(scope="module")
def connections():
    """Фикстура для подключения к базе данных 'connections' для dev stage или 'metaship для local stage'."""
    return DataBaseConnections()


@pytest.fixture(scope="module")
def customer_api():
    """Фикстура для подключения к базе данных 'customer-api'"""
    return DataBaseCustomerApi()


@pytest.fixture(scope="module")
def tracking_api():
    """Фикстура для подключения к базе данных 'tracking-api'"""
    return DataBaseTrackingApi()


@pytest.fixture(scope="module")
def widget_api():
    """Фикстура для подключения к базе данных 'widget-api'"""
    return DataBaseWidgetApi()


@pytest.fixture(scope="module", autouse=True)
def stop(app, request, connections, customer_api, tracking_api, widget_api):
    """Фикстура для завершения сессии"""
    def fin():
        app.close_session()
        for id_ in connections.get_list_shops():
            customer_api.delete_connection(shop_id=id_)
            widget_api.delete_widgets_id(shop_id=id_)
        for id_ in connections.get_list_orders():
            tracking_api.delete_list_orders_in_tracking(order_id=id_)
        connections.delete_all_setting()
        connections.close_database()
        customer_api.close_database()
        tracking_api.close_database()
        widget_api.close_database()
    request.addfinalizer(finalizer=fin)
