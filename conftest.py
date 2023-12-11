from databases.connections import DataBaseConnections
from databases.customer_api import DataBaseCustomerApi
from databases.tracking_api import DataBaseTrackingApi
from databases.widget_api import DataBaseWidgetApi
from fixture.application import Application
from fixture.admin import Admin
import pytest


@pytest.fixture(scope="module")
def app():
    """Фикстура для открытия сессии по Apiv2 metaship."""
    apiv2 = Application()
    apiv2.authorization.post_access_token()
    return apiv2


@pytest.fixture(scope="module")
def admin():
    """Фикстура для открытия сессии по Admin Api."""
    api_admin = Admin()
    api_admin.authorization.post_access_token(admin=True)
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
def stop(request, admin, app, connections, customer_api, tracking_api, widget_api):
    """Фикстура для завершения сессии"""
    def fin():
        admin.authorization.session.close()
        app.authorization.session.close()
        for id_ in connections.get_list_shops():
            customer_api.delete_connection(shop_id=id_)
            widget_api.delete_widgets_id(shop_id=id_)
        for id_ in connections.get_list_orders():
            tracking_api.delete_list_orders_in_tracking(order_id=id_)
        connections.delete_all_setting()
        connections.database.connection.close()
        customer_api.database.connection.close()
        tracking_api.database.connection.close()
        widget_api.database.connection.close()
    request.addfinalizer(finalizer=fin)
