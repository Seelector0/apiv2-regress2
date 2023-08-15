from utils.global_enums import INFO
from utils.checking import Checking
from environment import ENV_OBJECT
from random import choice
import pytest
import allure


@allure.description("Создание магазина")
def test_create_shop(app, connections):
    new_shop = app.shop.post_shop()
    Checking.check_status_code(response=new_shop, expected_status_code=201)
    Checking.checking_json_key(response=new_shop, expected_value=INFO.created_entity)
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_shops_value(shop_id=new_shop.json()["id"], value="deleted"),
        two_value=[False])
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_shops_value(shop_id=new_shop.json()["id"], value="visibility"),
        two_value=[True])


@allure.description("Создание склада")
def test_create_warehouse(app, connections):
    new_warehouse = app.warehouse.post_warehouse()
    Checking.check_status_code(response=new_warehouse, expected_status_code=201)
    Checking.checking_json_key(response=new_warehouse, expected_value=INFO.created_entity)
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_warehouses_value(warehouse_id=new_warehouse.json()["id"],
                                                                 value="deleted"),
        two_value=[False])
    Checking.check_value_comparison(
        one_value=connections.metaship.get_list_warehouses_value(warehouse_id=new_warehouse.json()["id"],
                                                                 value="visibility"),
        two_value=[True])


@allure.description("Подключение настроек СД Boxberry")
def test_integration_delivery_services(app):
    boxberry = app.service.delivery_services_boxberry()
    Checking.check_status_code(response=boxberry, expected_status_code=201)
    Checking.checking_json_key(response=boxberry, expected_value=INFO.created_entity)


@allure.description("Получение списка ПВЗ СД Boxberry")
def test_delivery_service_points(app):
    delivery_service_points = app.info.delivery_service_points(delivery_service_code="Boxberry")
    Checking.check_status_code(response=delivery_service_points, expected_status_code=200)
    Checking.checking_in_list_json_value(response=delivery_service_points, key_name="deliveryServiceCode",
                                         expected_value="Boxberry")


@allure.description("Получение списка точек сдачи СД Boxberry")
def test_intake_offices(app):
    intake_offices = app.info.intake_offices(delivery_service_code="Boxberry")
    Checking.check_status_code(response=intake_offices, expected_status_code=200)
    Checking.checking_in_list_json_value(response=intake_offices, key_name="deliveryServiceCode",
                                         expected_value="Boxberry")


@allure.description("Получения сроков доставки по СД Boxberry")
def test_delivery_time_schedules(app):
    delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="Boxberry")
    Checking.check_status_code(response=delivery_time_schedules, expected_status_code=200)
    Checking.checking_json_value(response=delivery_time_schedules, key_name="intervals",
                                 expected_value=INFO.boxberry_intervals)


@allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД Boxberry")
def test_info_vats(app):
    info_vats = app.info.info_vats(delivery_service_code="Boxberry")
    Checking.check_status_code(response=info_vats, expected_status_code=200)
    Checking.checking_json_key(response=info_vats, expected_value=INFO.boxberry_vats)


@allure.description("Получение актуального списка возможных сервисов заказа СД Boxberry")
def test_info_statuses(app):
    info_delivery_service_services = app.info.info_delivery_service_services(code="Boxberry")
    Checking.check_status_code(response=info_delivery_service_services, expected_status_code=200)
    Checking.checking_json_key(response=info_delivery_service_services, expected_value=INFO.boxberry_services)


@allure.description("Получение оферов в формате 'widget'")
def test_offers_format_widget(app):
    offers_widget = app.offers.get_offers(format_="widget")
    Checking.check_status_code(response=offers_widget, expected_status_code=200)
    Checking.check_delivery_services_in_widget_offers(response=offers_widget, delivery_service="Boxberry")


@allure.description("Получение Courier оферов по СД Boxberry")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_courier(app, payment_type):
    offers_courier = app.offers.get_offers(payment_type=payment_type, types="Courier", delivery_service_code="Boxberry")
    Checking.check_status_code(response=offers_courier, expected_status_code=200)
    Checking.checking_json_key(response=offers_courier, expected_value=["Courier"])


@allure.description("Получение оферов DeliveryPoint по СД Boxberry")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_offers_delivery_point(app, payment_type):
    offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
                                                  delivery_service_code="Boxberry")
    Checking.check_status_code(response=offers_delivery_point, expected_status_code=200)
    Checking.checking_json_key(response=offers_delivery_point, expected_value=["DeliveryPoint"])


@allure.description("Создание Courier многоместного заказа по CД Boxberry")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_multi_order_courier(app, payment_type, connections):
    new_order = app.order.post_multi_order(payment_type=payment_type, type_ds="Courier", service="Boxberry",
                                           declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание DeliveryPoint многоместного заказа по CД Boxberry")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_multi_delivery_point(app, payment_type, connections):
    new_order = app.order.post_multi_order(payment_type=payment_type, type_ds="DeliveryPoint", service="Boxberry",
                                           delivery_point_code="77717", declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание Courier заказа по CД Boxberry")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_courier(app, payment_type, connections):
    new_order = app.order.post_single_order(payment_type=payment_type, type_ds="Courier", service="Boxberry",
                                            declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание DeliveryPoint заказа по CД Boxberry")
@pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
def test_create_order_delivery_point(app, payment_type, connections):
    new_order = app.order.post_single_order(payment_type=payment_type, type_ds="DeliveryPoint", service="Boxberry",
                                            delivery_point_code="77717", declared_value=500)
    Checking.check_status_code(response=new_order, expected_status_code=201)
    Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
    connections.metaship.wait_create_order(order_id=new_order.json()["id"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="status"),
                                    two_value=["created"])
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=new_order.json()["id"],
                                                                                        value="state"),
                                    two_value=["succeeded"])


@allure.description("Создание заказа из файла СД Boxberry")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, file_extension, connections):
    new_orders = app.order.post_import_order_format_metaship(code="boxberry", file_extension=file_extension)
    Checking.check_status_code(response=new_orders, expected_status_code=200)
    for order in new_orders.json().values():
        connections.metaship.wait_create_order(order_id=order["id"])
        Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=order["id"],
                                                                                            value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=order["id"],
                                                                                            value="state"),
                                        two_value=["succeeded"])


@allure.description("Редактирование веса в заказе СД Boxberry")
def test_patch_order_weight(app, connections):
    random_order = choice(connections.metaship.get_list_all_orders())
    order_patch = app.order.patch_order(order_id=random_order, path="weight", weight=4)
    Checking.check_status_code(response=order_patch, expected_status_code=200)
    Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)


@allure.description("Удаление заказа CД Boxberry")
def test_delete_order(app, connections):
    random_order_id = choice(connections.metaship.get_list_all_orders())
    delete_order = app.order.delete_order(order_id=random_order_id)
    Checking.check_status_code(response=delete_order, expected_status_code=204)
    Checking.check_value_comparison(one_value=connections.metaship.get_list_order_value(order_id=random_order_id,
                                                                                        value="deleted"),
                                    two_value=[True])


@allure.description("Получения этикетки Boxberry вне партии")
@pytest.mark.skip("Проблема с моками")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_label_out_of_parcel(app, connections, labels):
    for order_id in connections.metaship.get_list_all_orders():
        label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение информации об истории изменения статусов заказа CД Boxberry")
def test_order_status(app, connections):
    for order_id in connections.metaship.get_list_all_orders():
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")


@allure.description("Получение подробной информации о заказе CД Boxberry")
def test_order_details(app, connections):
    for order_id in connections.metaship.get_list_all_orders():
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)


@allure.description("Создание партии CД Boxberry")
def test_create_parcel(app, connections):
    create_parcel = app.parcel.post_parcel(all_orders=True, order_id=connections.metaship.get_list_all_orders())
    Checking.check_status_code(response=create_parcel, expected_status_code=207)
    Checking.checking_in_list_json_value(response=create_parcel, key_name="type", expected_value="Parcel")


@allure.description("Получение этикетки CД Boxberry")
@pytest.mark.parametrize("labels", ["original", "termo"])
@pytest.mark.skip("Проблема с моками")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
def test_get_labels(app, connections, labels):
    for order_id in connections.metaship.get_list_all_orders_in_parcel():
        label = app.document.get_label(order_id=order_id, type_=labels)
        Checking.check_status_code(response=label, expected_status_code=200)


@allure.description("Получение этикеток заказов из партии СД Boxberry")
@pytest.mark.skip("Проблема с моками")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
def test_get_labels_from_parcel(app, connections):
    labels_from_parcel = app.document.post_labels(order_ids=connections.metaship.get_list_all_orders_in_parcel())
    Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)


@allure.description("Получение АПП CД Boxberry")
def test_get_app(app):
    acceptance = app.document.get_acceptance()
    Checking.check_status_code(response=acceptance, expected_status_code=200)


@allure.description("Получение документов CД Boxberry")
@pytest.mark.skipif(condition=f"{ENV_OBJECT.db_connections()}" == "metaship", reason="Тест только для dev стенда")
def test_get_documents(app):
    documents = app.document.get_files()
    Checking.check_status_code(response=documents, expected_status_code=200)


@allure.description("Создание забора СД Boxberry")
def test_create_intake(app, connections):
    new_intake = app.intakes.post_intakes(delivery_service="Boxberry")
    Checking.check_status_code(response=new_intake, expected_status_code=201)
    Checking.checking_json_key(response=new_intake, expected_value=INFO.created_entity)
    Checking.check_value_comparison(one_value=connections.metaship.get_list_intakes_value(
        intake_id=new_intake.json()["id"], value="status"), two_value=["created"])
