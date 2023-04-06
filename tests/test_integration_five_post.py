# from utils.checking import Checking
# from utils.enums.global_enums import INFO
# from random import choice
# import pytest
# import allure
#
#
# @allure.description("Создание магазина")
# def test_create_integration_shop(app, token):
#     result_new_shop = app.shop.post_shop()
#     Checking.check_status_code(response=result_new_shop, expected_status_code=201)
#     Checking.checking_json_key(response=result_new_shop, expected_value=INFO.created_entity)
#     result_get_new_shop = app.shop.get_shop_id(shop_id=result_new_shop.json()["id"])
#     Checking.check_status_code(response=result_get_new_shop, expected_status_code=200)
#     Checking.checking_json_value(response=result_get_new_shop, key_name="visibility", expected_value=True)
#
#
# @allure.description("Создание склада")
# def test_create_warehouse(app, token):
#     result_new_warehouse = app.warehouse.post_warehouse()
#     Checking.check_status_code(response=result_new_warehouse, expected_status_code=201)
#     Checking.checking_json_key(response=result_new_warehouse, expected_value=INFO.created_entity)
#     result_get_new_warehouse = app.warehouse.get_warehouse_id(warehouse_id=result_new_warehouse.json()["id"])
#     Checking.check_status_code(response=result_get_new_warehouse, expected_status_code=200)
#     Checking.checking_json_value(response=result_get_new_warehouse, key_name="visibility", expected_value=True)
#
#
# @allure.description("Подключение настроек службы доставки СД FivePost")
# def test_integration_delivery_services(app, token):
#     result_russian_post = app.service.delivery_services_five_post()
#     Checking.check_status_code(response=result_russian_post, expected_status_code=201)
#     Checking.checking_json_key(response=result_russian_post, expected_value=INFO.created_entity)
#     result_get_russian_post = app.service.get_delivery_services_code(code="FivePost")
#     Checking.check_status_code(response=result_get_russian_post, expected_status_code=200)
#     Checking.checking_json_value(response=result_get_russian_post, key_name="code", expected_value="FivePost")
#     Checking.checking_json_value(response=result_get_russian_post, key_name="credentials", field="visibility",
#                                  expected_value=True)
#
#
# @allure.description("Получение списка ПВЗ СД FivePost")
# def test_delivery_service_points(app, token):
#     result_delivery_service_points = app.info.delivery_service_points(delivery_service_code="FivePost")
#     Checking.check_status_code(response=result_delivery_service_points, expected_status_code=200)
#     Checking.checking_in_list_json_value(response=result_delivery_service_points, key_name="deliveryServiceCode",
#                                          expected_value="FivePost")
#
#
# @allure.description("Получения сроков доставки по СД FivePost")
# def test_delivery_time_schedules(app, token):
#     result_delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="FivePost")
#     Checking.check_status_code(response=result_delivery_time_schedules, expected_status_code=400)
#
#
# @allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД FivePost")
# def test_info_vats(app, token):
#     result_info_vats = app.info.info_vats(delivery_service_code="FivePost")
#     Checking.check_status_code(response=result_info_vats, expected_status_code=200)
#     Checking.checking_json_key(response=result_info_vats, expected_value=INFO.FIVE_POST_VATS)
#
#
# @allure.description("Получение оферов по СД FivePost (DeliveryPoint)")
# @pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
# def test_offers_delivery_point(app, payment_type, token):
#     result_offers_delivery_point = app.offers.get_offers(payment_type=payment_type, types="DeliveryPoint",
#                                                          delivery_service_code="FivePost",
#                                                          delivery_point_number="0014e8fe-1c2d-4429-b115-c9064ce54c30")
#     Checking.check_status_code(response=result_offers_delivery_point, expected_status_code=200)
#     Checking.checking_json_key(response=result_offers_delivery_point, expected_value=["DeliveryPoint"])
#
#
# @allure.description("Создание DeliveryPoint заказа по СД FivePost")
# @pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
# def test_create_delivery_point(app, payment_type, token):
#     result_order = app.order.post_order(payment_type=payment_type, type_ds="DeliveryPoint", service="FivePost",
#                                         delivery_point_code="0014e8fe-1c2d-4429-b115-c9064ce54c30", price=1000,
#                                         declared_value=1500)
#     Checking.check_status_code(response=result_order, expected_status_code=201)
#     Checking.checking_json_key(response=result_order, expected_value=INFO.created_entity)
#     result_get_order_by_id = app.order.get_order_id(order_id=result_order.json()["id"], sec=5)
#     Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
#     Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
#     Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")
#
#
# @allure.description("Получение информации об истории изменения статусов заказа СД FivePost")
# def test_order_status(app, token):
#     order_list_id = app.order.getting_order_id_out_parcel()
#     for order_id in order_list_id:
#         result_order_status = app.order.get_order_statuses(order_id=order_id)
#         Checking.check_status_code(response=result_order_status, expected_status_code=200)
#         Checking.checking_in_list_json_value(response=result_order_status, key_name="status", expected_value="created")
#
#
# @allure.description("Попытка получения этикетки СД FivePost вне партии")
# def test_get_label_of_parcel(app, token):
#     list_order_id = app.order.getting_order_id_out_parcel()
#     for order_id in list_order_id:
#         result_label = app.document.get_label(order_id=order_id)
#         Checking.check_status_code(response=result_label, expected_status_code=200)
#
#
# @allure.description("Попытка редактирования заказа СД FivePost")
# def test_editing_order(app, token):
#     order_list_id = app.order.getting_order_id_out_parcel()
#     result_order_put = app.order.put_order(order_id=choice(order_list_id), weight=5, length=12, width=14, height=11,
#                                            declared_value=2500, family_name="Иванов")
#     Checking.check_status_code(response=result_order_put, expected_status_code=400)
#
#
# @allure.description("Получение подробной информации о заказе СД FivePost")
# def test_order_details(app, token):
#     order_list_id = app.order.getting_order_id_out_parcel()
#     for order_id in order_list_id:
#         result_order_details = app.order.get_order_details(order_id=order_id)
#         Checking.check_status_code(response=result_order_details, expected_status_code=200)
#         Checking.checking_json_key(response=result_order_details, expected_value=INFO.details)
#
#
# @allure.description("Создание партии СД FivePost")
# def test_create_parcel(app, token):
#     orders_id = app.order.getting_order_id_out_parcel()
#     result_create_parcel = app.parcel.post_parcel(order_id=choice(orders_id))
#     Checking.check_status_code(response=result_create_parcel, expected_status_code=207)
#     Checking.checking_in_list_json_value(response=result_create_parcel, key_name="type", expected_value="Parcel")
#
#
# @allure.description("Редактирование партии СД FivePost (Добавление заказов)")
# def test_add_order_in_parcel(app, token):
#     parcel_id = app.parcel.getting_list_of_parcels_ids()
#     orders_id = app.order.getting_order_id_out_parcel()
#     for order in orders_id:
#         old_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
#         result_parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=parcel_id[0], op="add")
#         Checking.check_status_code(response=result_parcel_add, expected_status_code=200)
#         new_list_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
#         Checking.checking_sum_len_lists(old_list=old_list_order_in_parcel, new_list=new_list_order_in_parcel)
#
#
# @allure.description("Редактирование партии СД FivePost (Попытка изменение даты отправки партии)")
# def test_change_shipment_date(app, token):
#     parcel_id = app.parcel.getting_list_of_parcels_ids()
#     result_shipment_date = app.parcel.patch_parcel_shipment_date(parcel_id=parcel_id[0], day=5)
#     Checking.check_status_code(response=result_shipment_date, expected_status_code=422)
#
#
# @allure.description("Получение этикеток СД FivePost")
# def test_get_label(app, token):
#     parcel_id = app.parcel.getting_list_of_parcels_ids()
#     result_order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
#     for order_id in result_order_in_parcel:
#         result_label = app.document.get_label(order_id=order_id)
#         Checking.check_status_code(response=result_label, expected_status_code=200)
#
#
# @allure.description("Получение этикеток заказов из партии СД FivePost")
# def test_get_labels_from_parcel(app):
#     parcel_id = app.parcel.getting_list_of_parcels_ids()
#     order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
#     result_labels_from_parcel = app.document.post_labels(order_ids=order_in_parcel)
#     Checking.check_status_code(response=result_labels_from_parcel, expected_status_code=200)
#
#
# @allure.description("Получение АПП СД FivePost")
# def test_get_app(app, token):
#     result_app = app.document.get_acceptance()
#     Checking.check_status_code(response=result_app, expected_status_code=200)
#
#
# @allure.description("Получение документов СД FivePost")
# def test_get_documents(app, token):
#     result_documents = app.document.get_files()
#     Checking.check_status_code(response=result_documents, expected_status_code=200)
#
#
# @allure.description("Редактирование партииСД FivePost (Удаление заказа)")
# def test_remove_order_in_parcel(app, token):
#     parcel_id = app.parcel.getting_list_of_parcels_ids()
#     old_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
#     order_in_parcel = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
#     parcel_remove = app.parcel.patch_parcel(order_id=choice(order_in_parcel), parcel_id=parcel_id[0], op="remove")
#     new_list_order = app.parcel.get_orders_in_parcel(parcel_id=parcel_id[0])
#     Checking.check_status_code(response=parcel_remove, expected_status_code=200)
#     Checking.checking_difference_len_lists(old_list=old_list_order, new_list=new_list_order)
#
#
# @allure.description("Удаление заказа СД FivePost")
# def test_delete_order(app, token):
#     orders_id_list = app.order.getting_order_id_out_parcel()
#     random_order_id = choice(orders_id_list)
#     result_delete_order = app.order.delete_order(order_id=random_order_id)
#     Checking.check_status_code(response=result_delete_order, expected_status_code=204)
#     result_get_order_by_id = app.order.get_order_id(order_id=random_order_id)
#     Checking.check_status_code(response=result_get_order_by_id, expected_status_code=404)
