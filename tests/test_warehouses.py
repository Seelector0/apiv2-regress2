from utils.global_enums import INFO
from utils.checking import Checking
from random import choice
import allure
import pytest


@allure.description("Создание склада")
@pytest.mark.parametrize("execution_number", range(3))
def test_create_warehouse(app, execution_number):
    new_warehouse = app.warehouse.post_warehouse()
    Checking.check_status_code(response=new_warehouse, expected_status_code=201)
    Checking.checking_json_key(response=new_warehouse, expected_value=INFO.created_entity)


@allure.description("Получение списка складов")
def test_get_warehouses(app):
    list_warehouses = app.warehouse.get_warehouses()
    Checking.check_status_code(response=list_warehouses, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_warehouses)


@allure.description("Получение склада по его id")
def test_get_warehouse_by_id(app, connections):
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    warehouse = app.warehouse.get_warehouse_id(warehouse_id=random_warehouse_id)
    Checking.check_status_code(response=warehouse, expected_status_code=200)
    Checking.checking_json_key(response=warehouse, expected_value=INFO.entity_warehouse)


@allure.description("Обновление склада")
def test_put_warehouse(app, connections):
    working_time_warehouse = INFO.old_work_time_warehouse
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    put_warehouse = app.warehouse.put_warehouse(warehouse_id=random_warehouse_id, name="офигенный склад", pickup=False,
                                                comment="Такой себе склад", l_post_warehouse_id="99999",
                                                dpd_pickup_num="8324523", address="г Москва, пер 4-й Лесной, д 4",
                                                full_name="Виктор Виктор", phone="+79094563312",
                                                email="new_email@ya.ru", working_time=working_time_warehouse)
    Checking.check_status_code(response=put_warehouse, expected_status_code=204)
    assert_put_warehouse = app.warehouse.get_warehouse_id(warehouse_id=random_warehouse_id)
    Checking.check_status_code(response=assert_put_warehouse, expected_status_code=200)
    Checking.checking_json_key(response=assert_put_warehouse, expected_value=INFO.entity_warehouse)
    Checking.checking_json_value(response=assert_put_warehouse, key_name="name", expected_value="офигенный склад")
    Checking.checking_json_value(response=assert_put_warehouse, key_name="comment", expected_value="Такой себе склад")
    Checking.checking_json_value(response=assert_put_warehouse, key_name="lPostWarehouseId", expected_value="99999")
    Checking.checking_json_value(response=assert_put_warehouse, key_name="dpdPickupNum", expected_value="8324523")
    Checking.checking_json_value(response=assert_put_warehouse, key_name="contact", field="fullName",
                                 expected_value="Виктор Виктор")
    Checking.checking_json_value(response=assert_put_warehouse, key_name="contact", field="phone",
                                 expected_value="+79094563312")
    Checking.checking_json_value(response=assert_put_warehouse, key_name="contact", field="email",
                                 expected_value="new_email@ya.ru")
    Checking.checking_json_value(response=assert_put_warehouse, key_name="address", field="raw",
                                 expected_value="г Москва, пер 4-й Лесной, д 4")
    Checking.checking_json_value(response=assert_put_warehouse, key_name="workingTime",
                                 expected_value=working_time_warehouse)


@allure.description("Редактирование полей склада(visibility)")
def test_patch_warehouse_visibility(app, connections):
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    patch_warehouse = app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="visibility", value=False)
    Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=patch_warehouse, key_name="visibility", expected_value=False)


@allure.description("Редактирование полей склада(comment)")
def test_patch_warehouse_comment(app, connections):
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    patch_warehouse = app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="comment",
                                                    value="здесь могла быть ваша реклама")
    Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=patch_warehouse, key_name="comment",
                                 expected_value="здесь могла быть ваша реклама")


@allure.description("Редактирование полей склада(email)")
def test_patch_warehouse_email(app, connections):
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    patch_warehouse = app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="contact.email",
                                                    value="cool_email@ya.ru")
    Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=patch_warehouse, key_name="contact", field="email",
                                 expected_value="cool_email@ya.ru")


@allure.description("Редактирование полей склада(fullName)")
def test_patch_warehouse_full_name(app, connections):
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    patch_warehouse = app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="contact.fullName",
                                                    value="Гадя Петрович Хренова")
    Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=patch_warehouse, key_name="contact", field="fullName",
                                 expected_value="Гадя Петрович Хренова")


@allure.description("Редактирование полей склада(phone)")
def test_patch_warehouse_phone(app, connections):
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    patch_warehouse = app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="contact.phone",
                                                    value="+79095630011")
    Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=patch_warehouse, key_name="contact", field="phone",
                                 expected_value="+79095630011")


@allure.description("Редактирование полей склада(pickup)")
def test_patch_warehouse_pickup(app, connections):
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    patch_warehouse = app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="pickup", value=False)
    Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=patch_warehouse, key_name="pickup", expected_value=False)


@allure.description("Редактирование полей склада(dpdPickupNum)")
def test_patch_warehouse_dpd_pickup_num(app, connections):
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    patch_warehouse = app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="dpdPickupNum",
                                                    value="92929200")
    Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=patch_warehouse, key_name="dpdPickupNum", expected_value="92929200")


@allure.description("Редактирование полей склада(workingTime)")
def test_patch_warehouse_working_time(app, connections):
    working_time = INFO.new_work_time_warehouse
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    patch_warehouse = app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="workingTime",
                                                    value=working_time)
    Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=patch_warehouse, key_name="workingTime", expected_value=working_time)


@allure.description("Редактирование полей склада(lPostWarehouseId)")
def test_patch_warehouse_l_post_warehouse_id(app, connections):
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    patch_warehouse = app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="lPostWarehouseId",
                                                    value="123456")
    Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
    Checking.checking_json_value(response=patch_warehouse, key_name="lPostWarehouseId", expected_value="123456")


@allure.description("Удаление склада")
def test_delete_warehouse(app, connections):
    random_warehouse_id = choice(connections.metaship.get_list_warehouses())
    delete_warehouse = app.warehouse.delete_warehouse(warehouse_id=random_warehouse_id)
    Checking.check_status_code(response=delete_warehouse, expected_status_code=204)
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_warehouses_deleted(warehouse_id=random_warehouse_id), two_value=[True])
