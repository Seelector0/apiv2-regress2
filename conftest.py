from databases.connections import DataBaseConnections
from databases.customer_api import DataBaseCustomerApi
from databases.tracking_api import DataBaseTrackingApi
from databases.widget_api import DataBaseWidgetApi
from utils.helper.test_shops import TestsShop
from utils.helper.test_warehouses import TestsWarehouse
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
def shop_id(app):
    """Фикстура создания магазина"""
    tests_shop = TestsShop(app)
    shop_id = tests_shop.post_shop()
    return shop_id


@pytest.fixture(scope='module')
def shop_id_metaship(app):
    """Фикстура создания магазина для сд меташип"""
    tests_shop = TestsShop(app)
    shop_id_metaship = tests_shop.post_shop()
    return shop_id_metaship


@pytest.fixture(scope='module')
def warehouse_id(app):
    """Фикстура создания склада"""
    tests_warehouse = TestsWarehouse(app)
    warehouse_id = tests_warehouse.post_warehouse()
    return warehouse_id


@pytest.fixture(scope='module')
def warehouse_id_kz(app):
    """Фикстура создания склада для Казахстана"""
    tests_warehouse = TestsWarehouse(app)
    warehouse_id_kz = tests_warehouse.post_warehouse(country_code="KZ")
    return warehouse_id_kz
