from utils.global_enums import INFO
from utils.checking import Checking
from random import choice
import allure
import pytest


@allure.description("Создание магазина")
@pytest.mark.parametrize("execution_number", range(2))
def test_create_shop(app, execution_number):
    new_shop = app.shop.post_shop()
    Checking.check_status_code(response=new_shop, expected_status_code=201)
    Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)


@allure.description("Создание токена для виджета")
def test_create_token_for_widget(app, connections):
    for shop_id in connections.metaship.get_list_shops():
        token = app.widget.post_widget_tokens(shop_id=shop_id)
        Checking.check_status_code(response=token, expected_status_code=201)
        Checking.checking_json_key(response=token, expected_value=INFO.created_entity_widget)


@allure.description("Получение списка токенов")
def test_get_tokens(app):
    list_tokens = app.widget.get_widget_tokens()
    Checking.check_status_code(response=list_tokens, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_tokens)


@allure.description("Получение токена по его Id")
def test_get_token_by_id(app, widget_api, connections):
    widget_id = choice(widget_api.widget.get_widgets_id(shop_id=connections.metaship.get_list_shops()[0]))
    token_id = app.widget.get_widget_tokens_id(widget_id=widget_id)
    Checking.check_status_code(response=token_id, expected_status_code=200)
    Checking.checking_json_key(response=token_id, expected_value=INFO.entity_widget)
