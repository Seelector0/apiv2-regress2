from utils.api.delivery_serviches.delivery_services import ApiDeliveryServices
from utils.api.orders.orders import ApiOrder
from utils.api.parcels.parcels import ApiParcel
from utils.api.shops.shops import ApiShop
from utils.api.warehouses.warehouses import ApiWarehouse
from utils.checking import Checking
from random import randrange
import pytest
import allure


@allure.epic("Тесты Почты России по Интеграции")
class TestOrder:


    @allure.description("Создание магазина")
    def test_create_integration_shop(self, token):
        global result_new_shop
        result_new_shop = ApiShop.create_shop(shop_name=f"INT{randrange(100000, 999999)}", headers=token)
        Checking.check_status_code(response=result_new_shop, expected_status_code=201)
        Checking.checking_json_key(response=result_new_shop, expected_value=['id', 'type', 'url', 'status'])


    @allure.description("Создание склада")
    def test_create_new_warehouse(self, token):
        global result_new_warehouse
        result_new_warehouse = ApiWarehouse.create_warehouse(fullname="Виктор Викторович", headers=token)
        Checking.check_status_code(response=result_new_warehouse, expected_status_code=201)
        Checking.checking_json_key(response=result_new_warehouse, expected_value=['id', 'type', 'url', 'status'])



    @allure.description("Подключение настроек Почты России")
    def test_integration_russian_post(self, token):
        result_russian_post = ApiDeliveryServices.delivery_services_russian_post(connection_type="integration",
                                                                                 shop_id=result_new_shop.json()["id"],
                                                                                 headers=token)
        Checking.check_status_code(response=result_russian_post, expected_status_code=201)
        Checking.checking_json_key(response=result_russian_post, expected_value=['id', 'type', 'url', 'status'])


    @allure.description("Создание заказа")
    @pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
    def test_create_order_russian_post(self, payment_type, token):
        result_order = ApiOrder.create_order(warehouse_id=result_new_warehouse.json()["id"],
                                             shop_id=result_new_shop.json()["id"], payment_type=payment_type,
                                             type_ds="PostOffice", service="RussianPost", tariff="4", price=1000,
                                             declared_value=1500, headers=token)
        Checking.check_status_code(response=result_order, expected_status_code=201)
        Checking.checking_json_key(response=result_order, expected_value=['id', 'type', 'url', 'status'])


    @allure.description("Создание партии")
    def test_create_parcel_russian_post(self, token, connections):
        orders = connections.get_orders_list()
        result_parcel = ApiParcel.create_parcel(order_id=[i.order_id for i in orders], headers=token)
        Checking.check_status_code(response=result_parcel, expected_status_code=207)


    def test_clear_all_database(self, customer_api, connections, tracking_api):
        shops = connections.get_shops_list()
        for i in shops:
            customer_api.delete_connection(shop_id=i.shop_id)
        orders = connections.get_orders_list()
        for i in orders:
            tracking_api.delete_orders_list_in_tracking(order_id=i.order_id)
        connections.delete_all_setting()
