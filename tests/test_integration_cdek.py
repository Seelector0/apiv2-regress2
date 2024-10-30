import pytest
import allure
from random import choice
from utils.global_enums import INFO
from utils.common_tests import CommonConnections, CommonOffers, CommonOrders, CommonParcels, CommonInfo


@pytest.fixture(scope='module')
def shop_id(app, shared_data):
    return app.tests_shop.post_shop(shared_data=shared_data)


@allure.description("Подключение настроек службы доставки СД Cdek")
def test_integration_delivery_services(app, shop_id):
    CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                          connection_settings=app.settings.cdek())


@allure.description("Получение оферов в формате 'widget'")
@pytest.mark.not_parallel
def test_offers_format_widget(app, shop_id, warehouse_id):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, format_="widget",
                                    delivery_service_code="Cdek")


@allure.description("Получение оферов по СД Cdek")
@pytest.mark.parametrize("offer_type, payment_type",
                         [("Courier", "Paid"), ("Courier", "PayOnDelivery"),
                          ("DeliveryPoint", "Paid"), ("DeliveryPoint", "PayOnDelivery")])
def test_offers(app, shop_id, warehouse_id, offer_type, payment_type):
    CommonOffers.test_offers_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                    types=offer_type, delivery_service_code="Cdek", expected_value=[f"{offer_type}"])


@allure.description("Создание многоместного заказа по CД Cdek")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code, tariff",
                         [("Paid", "Courier", None, INFO.cdek_courier_tariffs),
                          ("PayOnDelivery", "Courier", None, INFO.cdek_courier_tariffs),
                          ("Paid", "DeliveryPoint", "MSK207", INFO.cdek_ds_tariffs),
                          ("PayOnDelivery", "DeliveryPoint", "MSK207", INFO.cdek_ds_tariffs)])
def test_create_multi_order(app, shop_id, warehouse_id, payment_type, delivery_type, tariff, delivery_point_code,
                            connections, shared_data):
    CommonOrders.test_multi_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                         payment_type=payment_type, delivery_type=delivery_type, service="Cdek",
                                         tariff=choice(tariff), delivery_point_code=delivery_point_code,
                                         shared_data=shared_data["cdek_i"]["order_ids"])


@allure.description("Добавление items в многоместный заказ СД Cdek")
def test_patch_multi_order(app, connections, shared_data):
    CommonOrders.test_patch_multi_order_common(app=app, delivery_service="Cdek", connections=connections,
                                               shared_data=shared_data["cdek_i"]["order_ids"])


@allure.description("Создание заказа по CД Cdek")
@pytest.mark.parametrize("payment_type, delivery_type, delivery_point_code, tariff",
                         [("Paid", "Courier", None, INFO.cdek_courier_tariffs),
                          ("PayOnDelivery", "Courier", None, INFO.cdek_courier_tariffs),
                          ("Paid", "DeliveryPoint", "MSK207", INFO.cdek_ds_tariffs),
                          ("PayOnDelivery", "DeliveryPoint", "MSK207", INFO.cdek_ds_tariffs)])
def test_create_single_order(app, shop_id, warehouse_id, payment_type, delivery_type, tariff, delivery_point_code,
                             connections, shared_data):
    CommonOrders.test_single_order_common(app=app, connections=connections, shop_id=shop_id, warehouse_id=warehouse_id,
                                          payment_type=payment_type, delivery_type=delivery_type, service="Cdek",
                                          tariff=choice(tariff),
                                          delivery_point_code=delivery_point_code,
                                          shared_data=shared_data["cdek_i"]["order_ids_single"])


@allure.description("Создание многоместного заказа из одноместного")
def test_patch_single_order(app, connections, shared_data):
    CommonOrders.test_patch_single_order_common(app=app, connections=connections,
                                                shared_data=shared_data["cdek_i"]["order_ids_single"],
                                                delivery_service="Cdek")


@pytest.mark.flaky(reruns=3, reruns_delay=2)
@allure.description("Создание заказа из файла СД Cdek")
@pytest.mark.parametrize("file_extension", ["xls", "xlsx"])
def test_create_order_from_file(app, shop_id, warehouse_id, file_extension, connections, shared_data):
    CommonOrders.test_create_order_from_file_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id,
                                                    connections=connections, code="cdek",
                                                    shared_data=shared_data["cdek_i"]["order_ids_single"],
                                                    file_extension=file_extension)


@allure.description("Получения сроков доставки по СД Cdek")
def test_delivery_time_schedules(app, shop_id, shared_data):
    CommonInfo.test_delivery_time_schedules_common(app=app, shop_id=shop_id, delivery_service_code="Cdek",
                                                   shared_data=shared_data["cdek_i"]["order_ids"])


@allure.description("Получение списка заказов CД Cdek")
def test_get_orders(app, shared_data):
    CommonOrders.test_get_orders_common(app=app, shared_delivery_service="cdek_i", shared_data=shared_data)


@allure.description("Получение информации о заказе CД Cdek")
def test_get_order_by_id(app, shared_data):
    CommonOrders.test_get_order_by_id_common(app=app, shared_data=shared_data["cdek_i"]["order_ids"])


@allure.description("Редактирование заказа СД Cdek")
def test_editing_order(app, connections, shared_data):
    CommonOrders.test_editing_order_place_common(app=app, connections=connections,
                                                 shared_data=shared_data["cdek_i"]["order_ids_single"])


@allure.description("Редактирование веса в заказе СД Cdek")
def test_patch_order_weight(app, connections, shared_data):
    CommonOrders.test_patch_order_weight_common(app=app, connections=connections, delivery_service="Cdek",
                                                shared_data=shared_data["cdek_i"]["order_ids_single"])


@allure.description("Редактирование информации о получателе в заказе СД Cdek")
def test_patch_order_recipient_cdek(app, connections, shared_data):
    CommonOrders.patch_order_recipient_common(app=app, connections=connections,
                                              shared_data=shared_data["cdek_i"]["order_ids"],
                                              family_name="Иванов", first_name="Авдотий", second_name="Николаевич",
                                              address={"raw": "119634, г Москва, ул. Лукинская, дом 5, кв. 23",
                                                       "countryCode": None})


@allure.description("Получение информации об истории изменения статусов заказа СД Cdek")
def test_order_status(app, shared_data):
    CommonOrders.test_order_status_common(app=app, shared_data=shared_data["cdek_i"]["order_ids"])


@allure.description("Удаление заказа СД Cdek")
def test_delete_order(app, connections, shared_data):
    CommonOrders.test_delete_order_common(app=app, connections=connections,
                                          shared_delivery_service="cdek_i", shared_data=shared_data)


@allure.description("Получения этикеток CД Cdek вне партии")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_labels_out_of_parcel(app, labels, shared_data):
    combined_order_ids = shared_data["cdek_i"]["order_ids"] + shared_data["cdek_i"]["order_ids_single"]
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, labels=labels, shared_data=combined_order_ids)


@allure.description("Получения оригинальных этикеток CД Cdek в формате A4, A5, A6 вне партии")
@pytest.mark.parametrize("format_", ["A4", "A5", "A6"])
def test_get_original_labels_out_of_parcel(app, format_, shared_data):
    combined_order_ids = shared_data["cdek_i"]["order_ids"] + shared_data["cdek_i"]["order_ids_single"]
    CommonOrders.test_get_labels_out_of_parcel_common(app=app, format_=format_, shared_data=combined_order_ids)


@allure.description("Получение подробной информации о заказе СД Cdek")
def test_order_details(app, shared_data):
    combined_order_ids = shared_data["cdek_i"]["order_ids"] + shared_data["cdek_i"]["order_ids_single"]
    CommonOrders.test_order_details_common(app=app, shared_data=combined_order_ids)


@allure.description("Создание партии СД Cdek")
def test_create_parcel(app, shared_data):
    CommonParcels.create_parcel_common(app=app, shared_data=shared_data, shared_delivery_service="cdek_i",
                                       types="order_ids_single")


@allure.description("Получение списка партий CД Cdek")
def test_get_parcels(app, shared_data):
    CommonParcels.test_get_parcels_common(app=app, shared_delivery_service="cdek_i", shared_data=shared_data)


@allure.description("Получение информации о партии CД Cdek")
def test_get_parcel_by_id(app, shared_data):
    CommonParcels.test_get_parcel_by_id_common(app=app, shared_data=shared_data["cdek_i"]["parcel_ids"])


@allure.description("Редактирование веса заказа в партии СД Cdek")
def test_patch_weight_random_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_patch_weight_random_order_in_parcel_common(app=app, connections=connections,
                                                                  shared_data=shared_data
                                                                  ["cdek_i"]["order_ids_in_parcel"])


@allure.description("Редактирование партии СД Cdek (Добавление заказов)")
def test_add_order_in_parcel(app, connections, shared_data):
    CommonParcels.add_order_in_parcel_common(app=app, connections=connections, shared_delivery_service="cdek_i",
                                             shared_data=shared_data)


@allure.description("Получение этикеток СД Cdek")
@pytest.mark.parametrize("labels", ["original", "termo"])
def test_get_label(app, labels, shared_data):
    CommonParcels.test_get_label_common(app=app, labels=labels,
                                        shared_data=shared_data["cdek_i"]["order_ids_in_parcel"])


@allure.description("Получения оригинальных этикеток CД Cdek в формате A4, A5, A6")
@pytest.mark.parametrize("format_", ["A4", "A5", "A6"])
def test_get_original_labels(app, format_, shared_data):
    CommonParcels.test_get_label_common(app=app, format_=format_,
                                        shared_data=shared_data["cdek_i"]["order_ids_in_parcel"])


@allure.description("Получение этикеток заказов из партии СД Cdek")
def test_get_labels_from_parcel(app, shared_data):
    CommonParcels.test_get_labels_from_parcel_common(app=app, shared_delivery_service="cdek_i", shared_data=shared_data)


@allure.description("Получение АПП СД Cdek")
def test_get_app(app, shared_data):
    CommonParcels.test_get_app_common(app=app, shared_data=shared_data["cdek_i"]["parcel_ids"])


@allure.description("Получение документов СД Cdek")
def test_get_documents(app, shared_data):
    CommonParcels.test_get_documents_common(app=app, shared_data=shared_data["cdek_i"]["parcel_ids"])


@allure.description("Создание формы с этикетками партии СД Cdek")
@pytest.mark.not_parallel
def test_forms_parcels_labels(app, shared_data):
    CommonParcels.test_forms_parcels_labels_common(app=app, shared_data=shared_data["cdek_i"]["parcel_ids"])


@allure.description("Редактирование партии СД Cdek (Удаление заказа)")
def test_remove_order_in_parcel(app, connections, shared_data):
    CommonParcels.test_remove_order_in_parcel_common(app=app, connections=connections, shared_delivery_service="cdek_i",
                                                     shared_data=shared_data)


@allure.description("Создание забора СД Cdek")
def test_create_intake(app, shop_id, warehouse_id, connections):
    CommonOrders.test_create_intake_common(app=app, shop_id=shop_id, warehouse_id=warehouse_id, connections=connections,
                                           delivery_service="Cdek")
