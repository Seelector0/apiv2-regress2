from utils.helper.test_shops import TestsShop
from utils.helper.test_warehouses import TestsWarehouse
import pytest


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
