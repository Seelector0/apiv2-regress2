import pytest
import allure
from utils.common_tests import CommonConnections, CommonInfo, CommonOffers, CommonOrders, CommonParcels


@allure.description("Подключение настроек службы доставки СД Halva")
def test_aggregation_delivery_services(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          connection_settings=app.settings.halva(aggregation=True),
                                                          moderation_settings=admin.moderation.halva)


@allure.description("Получение списка ПВЗ СД Halva")
def test_delivery_service_points(app, shop_id):
    CommonInfo.test_delivery_service_points_common(app=app, shop_id=shop_id, delivery_service_code="Halva")


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.not_parallel
def test_offers_format_widget(app, shop_id, warehouse_id):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, format_="widget",
                                    delivery_service_code="Halva")


@allure.description("Получение DeliveryPoint оферов по СД Halva")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, shop_id, warehouse_id, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types="DeliveryPoint", delivery_service_code="Halva",
                                    expected_value=["DeliveryPoint"])


@allure.description("Создание заказа по CД Halva")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code",
                         [
                             # ("Paid", "Courier", None), добавить как выкатим задачу 3445
                             # ("PayOnDelivery", "Courier", None),
                             ("Paid", "DeliveryPoint", "Халва-6193"),
                             ("PayOnDelivery", "DeliveryPoint", "Халва-6193")])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, delivery_type,
                             delivery_point_code, connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type=payment_type, delivery_type=delivery_type, service="Halva",
                                          delivery_point_code=delivery_point_code,
                                          shared_data=shared_data["order_ids"])


@allure.description("Редактирование заказа СД Halva")
def test_editing_order(app, shared_data):
    CommonOrders.test_editing_order_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение списка заказов CД Halva")
def test_get_orders(app):
    CommonOrders.test_get_orders_common(app=app)


@allure.description("Получение информации о заказе CД Halva")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получения этикетки Halva вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа CД Halva")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Получение подробной информации о заказе CД Halva")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["order_ids"])


@allure.description("Создание партии СД Halva")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение списка партий CД Halva")
def test_get_parcels(app):
    CommonParcels.test_get_parcels_common(app=app)


@allure.description("Получение информации о партии CД Halva")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД Halva (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    CommonParcels.add_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)


@allure.description("Получение этикеток СД Halva")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data)


@allure.description("Получение этикеток заказов из партии СД Halva")
def test_get_labels_from_parcel(app, shared_data):
    CommonParcels.test_get_labels_from_parcel_common(app=app, shared_data=shared_data)


@allure.description("Получение АПП СД Halva")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data)


@allure.description("Получение документов СД Halva")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data)


@allure.description("Создание формы с этикетками партии СД Halva")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data)


@allure.description("Редактирование партии СД Halva (Удаление заказа)")
def test_remove_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_remove_order_in_parcel_common(app=app, connections=connections, shared_data=shared_data)
