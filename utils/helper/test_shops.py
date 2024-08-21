from random import choice
from utils.global_enums import INFO
from utils.checking import Checking
import allure


class TestsShop:

    def __init__(self, app, connections):
        self.app = app
        self.connections = connections

    @allure.description("Создание магазина")
    def post_shop(self):
        """Создает магазин и возвращает его ID."""
        try:
            new_shop = self.app.shop.post_shop()
            Checking.check_status_code(response=new_shop, expected_status_code=201)
            Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)
            shop_id = new_shop.json().get('id')
            return shop_id
        except Exception as e:
            raise AssertionError(f"Ошибка при создании магазина: {e}")

    @allure.description("Получение списка магазинов")
    def get_shop(self):
        list_shops = self.app.shop.get_shops()
        Checking.check_status_code(response=list_shops, expected_status_code=200)
        Checking.check_response_is_not_empty(response=list_shops)

    @allure.description("Получение магазина по его id")
    def get_shop_by_id(self):
        random_shop_id = choice(self.connections.get_list_shops())
        shop = self.app.shop.get_shop_id(shop_id=random_shop_id)
        Checking.check_status_code(response=shop, expected_status_code=200)
        Checking.checking_json_key(response=shop, expected_value=INFO.entity_shops)

    @allure.description("Обновление магазина")
    def put_shop(self):
        random_shop_id = choice(self.connections.get_list_shops())
        put_shop = self.app.shop.put_shop(shop_id=random_shop_id, shop_name="new_shop_12345",
                                          shop_url="new_shop_url.su", contact_person="Кулебакин Максим Юрьевич",
                                          phone="79169326511")
        Checking.check_status_code(response=put_shop, expected_status_code=204)
        assert_put_shop = self.app.shop.get_shop_id(shop_id=random_shop_id)
        Checking.check_status_code(response=assert_put_shop, expected_status_code=200)
        Checking.checking_json_key(response=assert_put_shop, expected_value=INFO.entity_shops)
        Checking.checking_json_value(response=assert_put_shop, key_name="name", expected_value="new_shop_12345")
        Checking.checking_json_value(response=assert_put_shop, key_name="uri", expected_value="new_shop_url.su")
        Checking.checking_json_value(response=assert_put_shop, key_name="sender",
                                     expected_value="Кулебакин Максим Юрьевич")
        Checking.checking_json_value(response=assert_put_shop, key_name="phone", expected_value="79169326511")

    @allure.description("Редактирование полей магазина")
    def patch_shop(self):
        random_shop_id = choice(self.connections.get_list_shops())
        patch_shop = self.app.shop.patch_shop(shop_id=random_shop_id, value=False)
        Checking.check_status_code(response=patch_shop, expected_status_code=200)
        Checking.checking_json_value(response=patch_shop, key_name="visibility", expected_value=False)
