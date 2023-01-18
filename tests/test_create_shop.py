from utils.api.shops.shops import ApiShop
from utils.checking import Checking
from random import randrange
import allure


@allure.epic("Тесты создание, просмотр, изменение, удаление магазинов")
class TestShops:


    @allure.description("Создание нового магазина")
    def test_create_integration_shop(self, token, connections):
        result_post = ApiShop.create_shop(shop_name=f"INT{randrange(100000, 999999)}", headers=token)
        Checking.check_status_code(response=result_post, expected_status_code=201)
        Checking.checking_json_key(response=result_post, expected_value=['id', 'type', 'url', 'status'])


    @allure.description("Получение списка магазинов")
    def test_get_shop(self, token):
        result_get = ApiShop.get_shop(headers=token)
        Checking.check_status_code(response=result_get, expected_status_code=200)


    @allure.description("Поучение магазина по его id")
    def test_get_shop_by_id(self, token, connections):
        shop: list = connections.get_shops_list()
        for element in shop:
            result_get_by_id = ApiShop.get_shop_by_id(shop_id=element.shop_id, headers=token)
            Checking.check_status_code(response=result_get_by_id, expected_status_code=200)
            Checking.checking_json_key(response=result_get_by_id, expected_value=['id', 'number', 'name', 'uri', 'phone',
                                                                                  'sender', 'trackingTag', 'visibility'])


    @allure.description("Обновление магазина")
    def test_put_shop(self, token, connections):
        shop: list = connections.get_shops_list()
        for element in shop:
            uuid = element.shop_id
            result_put = ApiShop.put_shop(shop_id=uuid, headers=token, shop_name="123456")
            Checking.check_status_code(response=result_put, expected_status_code=204)
            result_get_by_id = ApiShop.get_shop_by_id(shop_id=uuid, headers=token)
            Checking.checking_json_value(response=result_get_by_id, key_name="name", expected_value="123456")


    @allure.description("Редактирование полей магазина")
    def test_patch_shop(self, token, connections):
        shop: list = connections.get_shops_list()
        for element in shop:
            result_patch = ApiShop.patch_shop(shop_id=element.shop_id, headers=token, value=False)
            Checking.check_status_code(response=result_patch, expected_status_code=200)
            Checking.checking_json_key(response=result_patch, expected_value=['id', 'number', 'name', 'uri', 'phone',
                                                                              'sender', 'trackingTag', 'visibility'])
            Checking.checking_json_value(response=result_patch, key_name="visibility", expected_value=False)


    def test_clear_all_database(self, customer_api, connections, tracking_api):
        shops = connections.get_shops_list()
        for i in shops:
            customer_api.delete_connection(shop_id=i.shop_id)
        orders = connections.get_orders_list()
        for i in orders:
            tracking_api.delete_orders_list_in_tracking(order_id=i.order_id)
        connections.delete_all_setting()
