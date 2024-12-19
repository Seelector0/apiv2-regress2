import allure
import pytest
from utils.common_tests import CommonConnections


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def shop_id_metaship(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(params=["shop_id", "shop_id_metaship"])
def param_shop_id(request):
    return request.getfixturevalue(request.param)


@pytest.fixture(scope='module')
def warehouse_id(app, connections, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(shared_data=shared_data)


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


@allure.description("Подключение настроек службы доставки интеграция")
@pytest.mark.parametrize("code, connection_settings",
                         [("RussianPost", lambda app: app.settings.russian_post()),
                          ("Cdek", lambda app: app.settings.cdek())])
def test_integration_delivery_services(app, shop_id, code, connection_settings):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id, code="RussianPost",
                                                          connection_settings=connection_settings(app))


@allure.description("Подключение настроек службы доставки агрегация")
@pytest.mark.parametrize("code, connection_settings, moderation_settings",
                         [("RussianPost", lambda app: app.settings.russian_post(aggregation=True),
                           lambda admin: admin.moderation.russian_post),
                          ("Cdek", lambda app: app.settings.cdek(aggregation=True),
                           lambda admin: admin.moderation.cdek)])
def test_aggregation_delivery_services(app, admin, shop_id_metaship, code, connection_settings, moderation_settings):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id_metaship,
                                                          code=code, connection_settings=connection_settings(app),
                                                          moderation_settings=moderation_settings(admin))


@allure.description("Получение списка выполненных настроек")
def test_get_delivery_services(app, param_shop_id):
    CommonConnections.test_get_delivery_services_common(app=app, shop_id=param_shop_id)


@allure.description("Редактирование полей настройки подключения к СД")
@pytest.mark.parametrize("code", ["RussianPost", "Cdek"])
def test_patch_delivery_service(app, param_shop_id, code):
    CommonConnections.test_patch_delivery_service_common(app=app, shop_id=param_shop_id, code=code)


@allure.description("Редактирование настройки подключения к СД")
@pytest.mark.parametrize("code", ["RussianPost", "Cdek"])
def test_put_delivery_service(app, shop_id, code):
    connection_settings, data = app.settings.get_connection_settings_and_data(code)
    CommonConnections.test_put_delivery_service_common(app=app, shop_id=shop_id, code=code,
                                                       connection_settings=connection_settings, data=data)


@allure.description("Деактивация настроек подключения к СД для ИМ")
@pytest.mark.parametrize("code", ["RussianPost", "Cdek"])
def test_deactivate_delivery_service(app, param_shop_id, code):
    CommonConnections.test_deactivate_delivery_service_common(app=app, shop_id=param_shop_id, code=code)


@allure.description("Активация настроек подключения к СД для ИМ")
@pytest.mark.parametrize("code", ["RussianPost", "Cdek"])
def test_activate_delivery_service(app, param_shop_id, code):
    CommonConnections.test_activate_delivery_service_common(app=app, shop_id=param_shop_id, code=code)


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


@allure.description("Создание веб-хука")
def test_post_webhook(app, shop_id, shared_data):
    app.tests_webhook.post_webhook(shop_id=shop_id, shared_data=shared_data)


@allure.description("Получения списка веб-хуков")
def test_get_webhooks(app):
    app.tests_webhook.get_webhooks()


@allure.description("Получения веб-хука по id")
def test_get_webhook_by_id(app, shared_data):
    app.tests_webhook.get_webhook_by_id(shared_data=shared_data)


@allure.description("Удаление веб-хука")
def test_delete_webhook(app, shared_data):
    app.tests_webhook.delete_webhook(shared_data=shared_data)
