from utils.checking import Checking
from utils.global_enums import INFO
from random import choice
import allure
import pytest


@allure.description("Создание магазина")
@pytest.mark.parametrize("execution_number", range(2))
def test_create_shop(app, execution_number):
    new_shop = app.shop.post_shop()
    Checking.check_status_code(response=new_shop, expected_status_code=201)
    Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)
    
    
@allure.description("Создание веб-хука")
def test_create_webhook(app, connections):
    for shop_id in connections.get_list_shops():
        webhooks = app.webhook.post_webhook(shop_id=shop_id)
        Checking.check_status_code(response=webhooks, expected_status_code=200)
        Checking.checking_json_key(response=webhooks, expected_value=INFO.entity_webhook)


@allure.description("Получение списка веб-хуков")
def test_get_webhooks(app):
    list_webhooks = app.webhook.get_webhooks()
    Checking.check_status_code(response=list_webhooks, expected_status_code=200)
    Checking.check_response_is_not_empty(response=list_webhooks)


@allure.description("Получение веб-хука по его Id")
def test_webhook_by_id(app, connections):
    random_webhook_id = choice(connections.get_list_webhook())
    webhook_id = app.webhook.get_webhook_id(webhook_id=random_webhook_id)
    Checking.check_status_code(response=webhook_id, expected_status_code=200)
    Checking.checking_json_key(response=webhook_id, expected_value=INFO.entity_webhook)
