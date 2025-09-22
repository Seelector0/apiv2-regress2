from utils.global_enums import INFO
from utils.checking import Checking
from utils.response_schemas import SCHEMAS
import allure


class TestsShop:

    def __init__(self, app):
        self.app = app

    @allure.description("Создание магазина")
    def post_shop(self, shared_data, shop_type="shop_id"):
        """Создает магазин и возвращает его ID."""
        try:
            new_shop = self.app.shop.post_shop()
            Checking.check_status_code(response=new_shop, expected_status_code=201)
            Checking.check_json_schema(response=new_shop, schema=SCHEMAS.shop.shop_create)
            shop_id = new_shop.json().get('id')
            shared_data[shop_type] = shop_id
            return shop_id
        except Exception as e:
            raise AssertionError(f"Ошибка при создании магазина: {e}")

    @allure.description("Получение списка магазинов")
    def get_shop(self):
        list_shops = self.app.shop.get_shops()
        Checking.check_status_code(response=list_shops, expected_status_code=200)
        Checking.check_json_schema(response=list_shops, schema=SCHEMAS.shop.shop_get)
        Checking.check_response_is_not_empty(response=list_shops)

    @allure.description("Получение магазина по его id")
    def get_shop_by_id(self, shop_id):
        shop = self.app.shop.get_shop_id(shop_id=shop_id)
        Checking.check_status_code(response=shop, expected_status_code=200)
        Checking.check_json_schema(response=shop, schema=SCHEMAS.shop.shop_get_by_id_or_editing)

    @allure.description("Обновление магазина")
    def put_shop(self, shop_id):
        put_shop = self.app.shop.put_shop(shop_id=shop_id, shop_name="new_shop_12345",
                                          shop_url="new_shop_url.su", contact_person="Кулебакин Максим Юрьевич",
                                          phone="79169326511")
        Checking.check_status_code(response=put_shop, expected_status_code=204)
        assert_put_shop = self.app.shop.get_shop_id(shop_id=shop_id)
        Checking.check_status_code(response=assert_put_shop, expected_status_code=200)
        Checking.checking_json_contains(response=assert_put_shop, expected_values=INFO.entity_shops)
        Checking.checking_json_value(response=assert_put_shop, key_name="name", expected_value="new_shop_12345")
        Checking.checking_json_value(response=assert_put_shop, key_name="uri", expected_value="new_shop_url.su")
        Checking.checking_json_value(response=assert_put_shop, key_name="sender",
                                     expected_value="Кулебакин Максим Юрьевич")
        Checking.checking_json_value(response=assert_put_shop, key_name="phone", expected_value="79169326511")

    @allure.description("Редактирование полей магазина")
    def patch_shop(self, shop_id):
        patch_shop = self.app.shop.patch_shop(shop_id=shop_id, value=False)
        Checking.check_status_code(response=patch_shop, expected_status_code=200)
        Checking.check_json_schema(response=patch_shop, schema=SCHEMAS.shop.shop_get_by_id_or_editing)
        Checking.checking_json_value(response=patch_shop, key_name="visibility", expected_value=False)

    @allure.description("Попытка удалить магазин и ожидание ошибки с кодом 409")
    def delete_shop(self, shop_id):
        delete_shop = self.app.shop.delete_shop(shop_id=shop_id)
        Checking.check_status_code(response=delete_shop, expected_status_code=409)
