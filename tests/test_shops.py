from utils.enums.global_enums import INFO
from utils.checking import Checking
from random import choice
import allure
import pytest

# Todo завести регрессионную задачу на метод PUT SHOP нужно возвращать 200 и тело ответа а не 204 как сейчас.


@allure.description("Создание магазина")
@pytest.mark.parametrize("execution_number", range(5))
def test_create_shop(app, token, execution_number):
    new_shop = app.shop.post_shop()
    Checking.check_status_code(response=new_shop, expected_status_code=201)
    Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)


@allure.description("Получение списка магазинов")
def test_get_shop(app, token):
    list_shops = app.shop.get_shops()
    Checking.check_status_code(response=list_shops, expected_status_code=200)
    for shop in list_shops.json():
        get_shop_by_id = app.shop.get_shop_id(shop_id=shop["id"])
        Checking.check_status_code(response=get_shop_by_id, expected_status_code=200)
        Checking.checking_json_key(response=get_shop_by_id, expected_value=INFO.entity_shops)


@allure.description("Получение магазина по его id")
def test_get_shop_by_id(app, token, connections):
    random_shop_id = choice(connections.metaship.get_list_shops())
    shop = app.shop.get_shop_id(shop_id=random_shop_id)
    Checking.check_status_code(response=shop, expected_status_code=200)
    Checking.checking_json_key(response=shop, expected_value=INFO.entity_shops)


@allure.description("Обновление магазина")
def test_put_shop(app, token,  connections):
    random_shop_id = choice(connections.metaship.get_list_shops())
    put_shop = app.shop.put_shop(shop_id=random_shop_id, shop_name="new_shop_12345", shop_url="new_shop_url.su",
                                 contact_person="Кулебакин Максим Юрьевич", phone="79169326511")
    Checking.check_status_code(response=put_shop, expected_status_code=204)
    assert_put_shop = app.shop.get_shop_id(shop_id=random_shop_id)
    Checking.check_status_code(response=assert_put_shop, expected_status_code=200)
    Checking.checking_json_key(response=assert_put_shop, expected_value=INFO.entity_shops)
    Checking.checking_json_value(response=assert_put_shop, key_name="name", expected_value="new_shop_12345")
    Checking.checking_json_value(response=assert_put_shop, key_name="uri", expected_value="new_shop_url.su")
    Checking.checking_json_value(response=assert_put_shop, key_name="sender", expected_value="Кулебакин Максим Юрьевич")
    Checking.checking_json_value(response=assert_put_shop, key_name="phone", expected_value="79169326511")


@allure.description("Редактирование полей магазина")
def test_patch_shop(app, token, connections):
    random_shop_id = choice(connections.metaship.get_list_shops())
    patch_shop = app.shop.patch_shop(shop_id=random_shop_id, value=False)
    Checking.check_status_code(response=patch_shop, expected_status_code=200)
    Checking.checking_json_value(response=patch_shop, key_name="visibility", expected_value=False)
