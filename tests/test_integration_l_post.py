import pytest
import allure
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels

@allure.description("Подключение настроек службы доставки СД LPost")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.l_post())


@allure.description("Получение оферов Courier по СД LPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, shop_id, warehouse_id, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types="Courier", delivery_service_code="LPost", expected_value=["Courier"])


@allure.description("Создание Courier многоместного заказа по CД LPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    if payment_type == "Paid":
        CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id,
                                             warehouse_id=warehouse_id,
                                             payment_type=payment_type, delivery_type="Courier", service="LPost",
                                             declared_value=0, delivery_sum=0,
                                             price_1=0, price_2=0, dimension=app.dicts.dimension(),
                                             shared_data=shared_data["order_ids"])
    else:
        CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id,
                                             warehouse_id=warehouse_id,
                                             payment_type=payment_type, delivery_type="Courier", service="LPost",
                                             price_1=500, price_2=500, dimension=app.dicts.dimension(),
                                             shared_data=shared_data["order_ids"])


@allure.description("Создание Courier заказа по СД LPost")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, shop_id, warehouse_id, payment_type, connections, shared_data):
    if payment_type == "Paid":
        CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id,
                                              warehouse_id=warehouse_id,
                                              payment_type=payment_type, delivery_type="Courier",
                                              service="LPost", declared_value=0, delivery_sum=0,
                                              price_1=0, price_2=0, price_3=0, shared_data=shared_data["order_ids"])

    else:
        CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id,
                                              warehouse_id=warehouse_id,
                                              payment_type=payment_type, delivery_type="Courier",
                                              service="LPost", shared_data=shared_data["order_ids"])


@allure.description("Получение списка заказов CД LPost")
def test_get_orders(app):
    CommonOrders.test_get_orders_common(app=app)


@allure.description("Получение информации о заказе CД LPost")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Редактирование заказа СД LPost")
def test_editing_order(app, shared_data):
    CommonOrders.test_editing_order_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД LPost")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Удаление заказа LPost")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получение подробной информации о заказе СД LPost")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии CД LPost")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение списка партий CД LPost")
def test_get_parcels(app):
    CommonParcels.test_get_parcels_common(app=app)


@allure.description("Получение информации о партии CД LPost")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП СД LPost")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД LPost")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД LPost")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)
