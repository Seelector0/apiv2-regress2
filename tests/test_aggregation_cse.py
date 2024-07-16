import pytest
import allure
from utils.dates import today
from utils.common_tests import CommonConnections, CommonInfo, CommonOffers, CommonOrders, CommonParcels


def test_aggregation_delivery_services(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          connection_settings=app.settings.cse(aggregation=True),
                                                          moderation_settings=admin.moderation.cse)


@allure.description("Получение списка ПВЗ СД Cse")
def test_delivery_service_points(app, shop_id):
    CommonInfo.test_delivery_service_points_common(app=app, shop_id=shop_id, delivery_service_code="Cse")


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.not_parallel
@pytest.mark.xfail
def test_offers_format_widget(app, shop_id, warehouse_id):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, format_="widget",
                                    delivery_service_code="Cse")


@allure.description("Получение оферов по СД Cse")
@pytest.mark.parametrize("offer_type, payment_type",
                         [("Courier", "Paid"), ("Courier", "PayOnDelivery"),
                          ("DeliveryPoint", "Paid"), ("DeliveryPoint", "PayOnDelivery")])
def test_offers(app, shop_id, warehouse_id, offer_type, payment_type):
    if offer_type == "DeliveryPoint":
        pytest.xfail("Ошибка, если атрибут в складе pickup == true")
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types=offer_type, delivery_service_code="Cse", expected_value=[f"{offer_type}"])


@allure.description("Создание многоместного заказа по CД Cse")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "0299ca01-ed73-11e8-80c9-7cd30aebf951"),
                          ("PayOnDelivery", "DeliveryPoint", "0299ca01-ed73-11e8-80c9-7cd30aebf951")])
def test_create_multi_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code,
                            connections, shared_data):
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                         payment_type=payment_type, delivery_type=delivery_type, service="Cse",
                                         tariff="64", delivery_point_code=delivery_point_code,
                                         date_pickup=str(today), dimension=app.dicts.dimension(),
                                         shared_data=shared_data["order_ids"])


@allure.description("Создание заказа по СД Cse")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [("Paid", "Courier", None),
                          ("PayOnDelivery", "Courier", None),
                          ("Paid", "DeliveryPoint", "0299ca01-ed73-11e8-80c9-7cd30aebf951"),
                          ("PayOnDelivery", "DeliveryPoint", "0299ca01-ed73-11e8-80c9-7cd30aebf951")])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, delivery_type, delivery_point_code,
                             connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type=payment_type, delivery_type=delivery_type, service="Cse",
                                          tariff="64", delivery_point_code=delivery_point_code,
                                          date_pickup=str(today),
                                          shared_data=shared_data["order_ids"])


@allure.description("Получение списка заказов CД Cse")
def test_get_orders(app):
    CommonOrders.test_get_orders_common(app=app)


@allure.description("Получение информации о заказе CД Cse")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа СД Cse")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Удаление заказа СД Cse")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получения этикеток CД Cse вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе СД Cse")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии СД Cse")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение списка партий CД Cse")
def test_get_parcels(app):
    CommonParcels.test_get_parcels_common(app=app)


@allure.description("Получение информации о партии CД Cse")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД Cse (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    CommonParcels.add_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получение этикеток СД Cse")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП СД Cse")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД Cse")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД Cse")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД Cse (Удаление заказа)")
def test_remove_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_remove_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Создание забора СД Cse")
def test_create_intake(app, shop_id, warehouse_id, connections):
    CommonOrders.test_create_intake_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, connections=connections,
                                           delivery_service="Cse")
