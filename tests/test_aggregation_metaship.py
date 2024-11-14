import pytest
import allure
from utils.environment import ENV_OBJECT
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@pytest.fixture(scope='module')
def shop_id_metaship(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data, shop_type="shop_id_metaship")


@allure.description("Подключение настроек службы доставки СД MetaShip")
def test_aggregation_delivery_services_boxberry(app, admin, shop_id):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id,
                                                          connection_settings=app.settings.boxberry(aggregation=True),
                                                          moderation_settings=admin.moderation.boxberry)


def test_aggregation_delivery_services_metaship(app, admin, shop_id, shop_id_metaship):
    CommonConnections.connect_aggregation_services_common(app=app, admin=admin, shop_id=shop_id_metaship,
                                                          delivery_service="MetaShip",
                                                          connection_settings=app.settings.metaship(),
                                                          update_settings=admin.dicts.form_settings_ds_metaship
                                                          (shop_id=shop_id),
                                                          moderation_settings=admin.moderation.metaship)


@pytest.mark.skipif(condition=ENV_OBJECT.db_connections() == "metaship", reason="Тест только для dev стенда")
@allure.description("Получение Courier оферов по СД MetaShip")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, shop_id_metaship, warehouse_id, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id_metaship, warehouse_id=warehouse_id,
                                    payment_type=payment_type, types="Courier", delivery_service_code="MetaShip",
                                    expected_value=["Courier"])


@allure.description("Создание Courier заказа по CД MetaShip")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
@pytest.mark.parametrize("execution_number", range(2))
def test_create_order_courier(app, shop_id_metaship, warehouse_id, payment_type, connections, execution_number,
                              shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id_metaship,
                                          warehouse_id=warehouse_id, payment_type=payment_type,
                                          delivery_type="Courier", service="MetaShip",
                                          shared_data=shared_data["metaship_a"]["order_ids"])


@allure.description("Получение списка заказов CД MetaShip")
def test_get_orders(app, shared_data):
    CommonOrders.test_get_orders_common(app=app, shared_delivery_service="metaship_a", shared_data=shared_data)


@allure.description("Получение информации о заказе CД MetaShip")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["metaship_a"]["order_ids"])


@allure.description("Редактирование веса в заказе СД MetaShip")
def test_patch_order_weight(app, connections, shared_data):
    CommonOrders.test_patch_order_weight_common(app=app, connections=connections,
                                                shared_data=shared_data["metaship_a"]["order_ids"])


@allure.description("Удаление заказа CД MetaShip")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections, shared_delivery_service="metaship_a",
                                          shared_data=shared_data)


@allure.description("Получения этикетки MetaShip вне партии")
def test_get_labels_out_of_parcel(app, shared_data):
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, shared_data=shared_data["metaship_a"]["order_ids"])


@allure.description("Получение информации об истории изменения статусов заказа CД MetaShip")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["metaship_a"]["order_ids"])


@allure.description("Получение подробной информации о заказе CД MetaShip")
def test_order_details(app, shared_data):
    CommonOrders.test_order_details_common(app=app, shared_data=shared_data["metaship_a"]["order_ids"])


@allure.description("Создание партии CД MetaShip")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_delivery_service="metaship_a", shared_data=shared_data)


@allure.description("Получение списка партий CД MetaShip")
def test_get_parcels(app, shared_data):
    CommonParcels.test_get_parcels_common(app=app, shared_delivery_service="metaship_a", shared_data=shared_data)


@allure.description("Получение информации о партии CД MetaShip")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data["metaship_a"]["parcel_ids"])


@allure.description("Получение этикетки CД MetaShip")
def test_get_label(app, shared_data):
    CommonParcels.test_get_label_common(app=app, shared_data=shared_data["metaship_a"]["order_ids_in_parcel"])


@allure.description("Получение этикеток заказов из партии СД MetaShip")
def test_get_labels_from_parcel(app, shared_data):
    CommonParcels.test_get_labels_from_parcel_common(app=app, shared_delivery_service="metaship_a",
                                                     shared_data=shared_data)


@allure.description("Получение АПП CД MetaShip")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data["metaship_a"]["parcel_ids"])


@allure.description("Получение документов CД MetaShip")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data["metaship_a"]["parcel_ids"])


@allure.description("Создание формы с этикетками партии СД MetaShip")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data["metaship_a"]["parcel_ids"])
