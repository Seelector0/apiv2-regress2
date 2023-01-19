from utils.api.warehouses.warehouses import ApiWarehouse
from utils.checking import Checking
import allure


@allure.epic("Создание, просмотр, изменение, удаление складов")
class TestWarehouses:


    @allure.description("Создание склада")
    def test_create_new_warehouse(self, token, connections):
        result_post = ApiWarehouse.create_warehouse(fullname="Виктор Викторович", headers=token)
        Checking.check_status_code(response=result_post, expected_status_code=201)
        Checking.checking_json_key(response=result_post, expected_value=['id', 'type', 'url', 'status'])


    @allure.description("Получение списка магазинов")
    def test_get_warehouses(self, token):
        result_get = ApiWarehouse.get_warehouses(headers=token)
        Checking.check_status_code(response=result_get, expected_status_code=200)


    @allure.description("Получение склада по его 'id'")
    def test_get_warehouse_by_id(self, connections, token):
        warehouse = connections.get_warehouses_list()
        for element in warehouse:
            result_by_id = ApiWarehouse.get_warehouse_by_id(headers=token, warehouse_id=element.warehouse_id)
            Checking.check_status_code(response=result_by_id, expected_status_code=200)
            Checking.checking_json_key(response=result_by_id, expected_value=['id', 'number', 'name', 'visibility',
                                                                              'address', 'contact', 'workingTime',
                                                                              'pickup', 'dpdPickupNum', 'comment'])


    @allure.description("Обновление склада")
    def test_put_warehouse(self, connections, token):
        warehouse = connections.get_warehouses_list()
        for element in warehouse:
            uuid = element.warehouse_id
            result_put = ApiWarehouse.put_warehouse(headers=token, warehouse_id=uuid, fullname="Ваня Ваня")
            Checking.check_status_code(response=result_put, expected_status_code=204)
            result_get_by_id = ApiWarehouse.get_warehouse_by_id(warehouse_id=uuid, headers=token)
            Checking.checking_json_value(response=result_get_by_id, key_name="contact", field='fullName', expected_value="Ваня Ваня")

    @allure.description("Удаление склада")
    def test_delete_warehouse(self, connections, token):
        warehouse = connections.get_warehouses_list()
        for element in warehouse:
            uuid = element.warehouse_id
            result_delete = ApiWarehouse.delete_warehouse(headers=token, warehouse_id=uuid)
            Checking.check_status_code(response=result_delete, expected_status_code=204)
            result_get_by_id = ApiWarehouse.get_warehouse_by_id(warehouse_id=uuid, headers=token)
            Checking.check_status_code(response=result_get_by_id, expected_status_code=404)
