import allure
import pytest


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@allure.description("Получение магазина по его id")
def test_get_shop_by_id(app, shop_id):
    app.tests_shop.get_shop_by_id(shop_id=shop_id)


@allure.description("Получение списка магазинов")
def test_get_shop(app):
    app.tests_shop.get_shop()


@allure.description("Обновление магазина")
def test_put_shop(app, shop_id):
    app.tests_shop.put_shop(shop_id=shop_id)


@allure.description("Редактирование полей магазина")
def test_patch_shop(app, shop_id):
    app.tests_shop.patch_shop(shop_id=shop_id)


@allure.description("Получение склада по его id")
def test_warehouse_by_id(app, warehouse_id):
    app.tests_warehouse.warehouse_by_id(warehouse_id=warehouse_id)


@allure.description("Получение списка складов")
def test_get_warehouses(app):
    app.tests_warehouse.get_warehouses()


@allure.description("Обновление склада")
def test_put_warehouse(app, warehouse_id):
    app.tests_warehouse.put_warehouse(warehouse_id=warehouse_id)


@allure.description("Редактирование полей склада")
def test_patch_warehouse(app, warehouse_id):
    app.tests_warehouse.patch_warehouse(warehouse_id=warehouse_id)


@allure.description("Удаление склада")
def test_delete_warehouse(app, warehouse_id):
    app.tests_warehouse.delete_warehouse(warehouse_id=warehouse_id)
