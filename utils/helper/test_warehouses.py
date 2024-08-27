from utils.global_enums import INFO
from utils.checking import Checking
from random import choice
import allure


class TestsWarehouse:

    def __init__(self, app, connections):
        self.app = app
        self.connections = connections

    @allure.description("Создание склада")
    def post_warehouse(self, country_code: str = None, pickup: bool = None):
        try:
            new_warehouse = self.app.warehouse.post_warehouse(country_code=country_code, pickup=pickup)
            Checking.check_status_code(response=new_warehouse, expected_status_code=201)
            Checking.checking_json_key(response=new_warehouse, expected_value=INFO.created_entity)
            warehouse_id = new_warehouse.json().get('id')
            return warehouse_id
        except Exception as e:
            raise AssertionError(f"Ошибка при создании склада: {e}")

    @allure.description("Получение списка складов")
    def get_warehouses(self):
        list_warehouses = self.app.warehouse.get_warehouses()
        Checking.check_status_code(response=list_warehouses, expected_status_code=200)
        Checking.check_response_is_not_empty(response=list_warehouses)

    @allure.description("Получение склада по его id")
    def warehouse_by_id(self):
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        warehouse = self.app.warehouse.get_warehouse_id(warehouse_id=random_warehouse_id)
        Checking.check_status_code(response=warehouse, expected_status_code=200)
        Checking.checking_json_key(response=warehouse, expected_value=INFO.entity_warehouse)

    @allure.description("Обновление склада")
    def put_warehouse(self):
        working_time_warehouse = INFO.old_work_time_warehouse
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        put_warehouse = self.app.warehouse.put_warehouse(warehouse_id=random_warehouse_id, name="офигенный склад",
                                                         pickup=False, comment="Такой себе склад",
                                                         l_post_warehouse_id="99999", dpd_pickup_num="8324523",
                                                         address="г Москва, пер 4-й Лесной, д 4",
                                                         full_name="Виктор Виктор", phone="+79094563312",
                                                         email="new_email@ya.ru", working_time=working_time_warehouse)
        Checking.check_status_code(response=put_warehouse, expected_status_code=204)
        assert_put_warehouse = self.app.warehouse.get_warehouse_id(warehouse_id=random_warehouse_id)
        Checking.check_status_code(response=assert_put_warehouse, expected_status_code=200)
        Checking.checking_json_key(response=assert_put_warehouse, expected_value=INFO.entity_warehouse)
        Checking.checking_json_value(response=assert_put_warehouse, key_name="name", expected_value="офигенный склад")
        Checking.checking_json_value(response=assert_put_warehouse, key_name="comment",
                                     expected_value="Такой себе склад")
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
    def patch_warehouse_visibility(self):
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        patch_warehouse = self.app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="visibility",
                                                             value=False)
        Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
        Checking.checking_json_value(response=patch_warehouse, key_name="visibility", expected_value=False)

    @allure.description("Редактирование полей склада(comment)")
    def patch_warehouse_comment(self):
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        patch_warehouse = self.app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="comment",
                                                             value="здесь могла быть ваша реклама")
        Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
        Checking.checking_json_value(response=patch_warehouse, key_name="comment",
                                     expected_value="здесь могла быть ваша реклама")

    @allure.description("Редактирование полей склада(email)")
    def patch_warehouse_email(self):
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        patch_warehouse = self.app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="contact.email",
                                                             value="cool_email@ya.ru")
        Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
        Checking.checking_json_value(response=patch_warehouse, key_name="contact", field="email",
                                     expected_value="cool_email@ya.ru")

    @allure.description("Редактирование полей склада(fullName)")
    def patch_warehouse_full_name(self):
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        patch_warehouse = self.app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="contact.fullName",
                                                             value="Гадя Петрович Хренова")
        Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
        Checking.checking_json_value(response=patch_warehouse, key_name="contact", field="fullName",
                                     expected_value="Гадя Петрович Хренова")

    @allure.description("Редактирование полей склада(phone)")
    def patch_warehouse_phone(self):
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        patch_warehouse = self.app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="contact.phone",
                                                             value="+79095630011")
        Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
        Checking.checking_json_value(response=patch_warehouse, key_name="contact", field="phone",
                                     expected_value="+79095630011")

    @allure.description("Редактирование полей склада(pickup)")
    def patch_warehouse_pickup(self):
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        patch_warehouse = self.app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="pickup",
                                                             value=False)
        Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
        Checking.checking_json_value(response=patch_warehouse, key_name="pickup", expected_value=False)

    @allure.description("Редактирование полей склада(dpdPickupNum)")
    def patch_warehouse_dpd_pickup_num(self):
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        patch_warehouse = self.app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="dpdPickupNum",
                                                             value="92929200")
        Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
        Checking.checking_json_value(response=patch_warehouse, key_name="dpdPickupNum", expected_value="92929200")

    @allure.description("Редактирование полей склада(workingTime)")
    def patch_warehouse_working_time(self):
        working_time = INFO.new_work_time_warehouse
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        patch_warehouse = self.app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="workingTime",
                                                             value=working_time)
        Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
        Checking.checking_json_value(response=patch_warehouse, key_name="workingTime", expected_value=working_time)

    @allure.description("Редактирование полей склада(lPostWarehouseId)")
    def patch_warehouse_l_post_warehouse_id(self):
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        patch_warehouse = self.app.warehouse.patch_warehouse(warehouse_id=random_warehouse_id, path="lPostWarehouseId",
                                                             value="123456")
        Checking.check_status_code(response=patch_warehouse, expected_status_code=200)
        Checking.checking_json_value(response=patch_warehouse, key_name="lPostWarehouseId", expected_value="123456")

    @allure.description("Удаление склада")
    def delete_warehouse(self):
        random_warehouse_id = choice(self.connections.get_list_warehouses())
        delete_warehouse = self.app.warehouse.delete_warehouse(warehouse_id=random_warehouse_id)
        Checking.check_status_code(response=delete_warehouse, expected_status_code=204)
        Checking.check_value_comparison(responses={"DELETE v2/customer/warehouses/{id}": delete_warehouse},
                                        one_value=self.connections.get_list_warehouses_value
                                        (warehouse_id=random_warehouse_id, value="deleted"), two_value=[True])
