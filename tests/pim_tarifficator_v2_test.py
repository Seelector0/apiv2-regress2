import pytest
import allure
from random import choice
from utils.global_enums import INFO
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def warehouse_id(app, connections, shared_data):
    """Фикстура создания склада"""
    return app.tests_warehouse.post_warehouse(shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД RussianPost")
def test_aggregation_delivery_services_russian_post(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          delivery_service="RussianPost",
                                                          connection_settings=app.settings.russian_post
                                                          (aggregation=True),
                                                          update_settings=admin.dicts.form_settings_ds_russian_post
                                                          (pim_tariff_v2=True),
                                                          moderation_settings=admin.moderation.russian_post)


@allure.description("Подключение настроек службы доставки СД FivePost")
def test_aggregation_delivery_services_five_post(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          delivery_service="FivePost",
                                                          connection_settings=app.settings.five_post(aggregation=True),
                                                          update_settings=admin.dicts.form_settings_ds_five_post
                                                          (pim_tariff_v2=True),
                                                          moderation_settings=admin.moderation.five_post)


@allure.description("Получение оферов по СД RussianPost")
@pytest.mark.parametrize("offer_type, payment_type", [("Courier", "Paid"), ("Courier", "PayOnDelivery"),
                                                      ("PostOffice", "Paid"), ("PostOffice", "PayOnDelivery")])
def test_offers_russian_post(app, shop_id, warehouse_id, offer_type, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types=offer_type, delivery_service_code="RussianPost",
                                    expected_value=[f"{offer_type}"])


@allure.description("Получение оферов по СД FivePost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_five_post(app, shop_id, warehouse_id, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types="DeliveryPoint", delivery_service_code="FivePost",
                                    delivery_point_number="006bf88a-5186-45d9-9911-89d37f1edc86",
                                    expected_value=["DeliveryPoint"])
