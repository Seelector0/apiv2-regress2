from random import randrange
from utils.api.delivery_serviches.delivery_services import ApiDeliveryServices
from utils.api.shops.shops import ApiShop
from utils.checking import Checking
import allure


@allure.epic("Создание, просмотр, изменение, удаление, активация и деактивация настроек служб доставок")
class TestDeliveryServices:


    @allure.description("Создание нового магазина для подключения к нему СД")
    def test_create_integration_shop(self, token, connections):
        result_post = ApiShop.create_shop(shop_name=f"INT{randrange(100000, 999999)}", headers=token)
        Checking.check_status_code(response=result_post, expected_status_code=201)
        Checking.checking_json_key(response=result_post, expected_value=['id', 'type', 'url', 'status'])


    @allure.description("Подключение настроек Почты России")
    def test_integration_russian_post(self, token, connections):
        shop_list = connections.get_shops_list()
        for element in shop_list:
            result_post = ApiDeliveryServices.delivery_services_russian_post(
                connection_type="integration", shop_id=element.shop_id, headers=token)
            Checking.check_status_code(response=result_post, expected_status_code=201)
            Checking.checking_json_key(response=result_post, expected_value=['id', 'type', 'url', 'status'])
