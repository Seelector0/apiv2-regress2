from utils.checking import Checking
from random import choice
import pytest
import allure


@allure.epic("Тесты Почты России по Интеграции")
class TestRussianPostIntegration:

    @allure.description("Создание магазина")
    def test_create_integration_shop(self, app, token):
        result_new_shop = app.shop.create_shop(headers=token)
        Checking.check_status_code(response=result_new_shop, expected_status_code=201)
        Checking.checking_json_key(response=result_new_shop, expected_value=['id', 'type', 'url', 'status'])
        result_get_new_shop = app.shop.get_shop_by_id(shop_id=result_new_shop.json()["id"], headers=token)
        Checking.check_status_code(response=result_get_new_shop, expected_status_code=200)
        Checking.checking_json_value(response=result_get_new_shop, key_name="visibility", expected_value=True)

    @allure.description("Создание склада")
    def test_create_new_warehouse(self, app, token):
        result_new_warehouse = app.warehouse.create_warehouse(fullname="Виктор Викторович", headers=token)
        Checking.check_status_code(response=result_new_warehouse, expected_status_code=201)
        Checking.checking_json_key(response=result_new_warehouse, expected_value=['id', 'type', 'url', 'status'])
        result_get_new_warehouse = app.warehouse.get_warehouse_by_id(warehouse_id=result_new_warehouse.json()["id"],
                                                                     headers=token)
        Checking.check_status_code(response=result_get_new_warehouse, expected_status_code=200)
        Checking.checking_json_value(response=result_get_new_warehouse, key_name="visibility", expected_value=True)

    @allure.description("Подключение настроек Почты России")
    def test_integration_russian_post(self, app, token):
        shop_id = app.shop.get_shops_id(headers=token)
        result_russian_post = app.service.delivery_services_russian_post(connection_type="integration",
                                                                         shop_id=shop_id[0], headers=token)
        Checking.check_status_code(response=result_russian_post, expected_status_code=201)
        Checking.checking_json_key(response=result_russian_post, expected_value=['id', 'type', 'url', 'status'])
        result_get_russian_post = app.service.get_delivery_services_code(shop_id=shop_id[0], code="RussianPost",
                                                                         headers=token)
        Checking.check_status_code(response=result_get_russian_post, expected_status_code=200)
        Checking.checking_json_value(response=result_get_russian_post, key_name="code", expected_value="RussianPost")
        Checking.checking_json_value(response=result_get_russian_post, key_name="credentials", field="visibility",
                                     expected_value=True)

    @allure.description("Получение списка ПВЗ СД Почты России")
    def test_delivery_service_points(self, app, token):
        shop_id = app.shop.get_shops_id(headers=token)
        result_delivery_service_points = app.info.delivery_service_points(delivery_service_code="RussianPost",
                                                                          shop_id=shop_id[0], headers=token)
        Checking.check_status_code(response=result_delivery_service_points, expected_status_code=200)
        Checking.checking_in_list_json_value(response=result_delivery_service_points, key_name="deliveryServiceCode",
                                             expected_value="RussianPost")

    @allure.description("Получение списка точек сдачи СД Почты России")
    def test_intake_offices(self, app, token):
        result_intake_offices = app.info.intake_offices(delivery_service_code="RussianPost", limit=10, headers=token)
        Checking.check_status_code(response=result_intake_offices, expected_status_code=200)
        Checking.checking_in_list_json_value(response=result_intake_offices, key_name="deliveryServiceCode",
                                             expected_value="RussianPost")

    @allure.description("Получения сроков доставки по Почте России")
    def test_delivery_time_schedules(self, app, token):
        result_delivery_time_schedules = app.info.delivery_time_schedules(delivery_service_code="RussianPost",
                                                                          headers=token)
        Checking.check_status_code(response=result_delivery_time_schedules, expected_status_code=200)
        Checking.checking_json_key(response=result_delivery_time_schedules, expected_value=['schedule', 'intervals'])

    @allure.description("Получение списка ставок НДС, которые умеет принимать и обрабатывать СД Почта России")
    def test_info_vats(self, app, token):
        result_info_vats = app.info.info_vats(delivery_service_code="RussianPost", headers=token)
        Checking.check_status_code(response=result_info_vats, expected_status_code=200)
        Checking.checking_json_key(response=result_info_vats, expected_value=[{'code': 'NO_VAT', 'name': 'Без НДС'},
                                                                              {'code': '0', 'name': 'НДС 0%'},
                                                                              {'code': '10', 'name': 'НДС 10%'},
                                                                              {'code': '20', 'name': 'НДС 20%'},
                                                                              {'code': '10/110', 'name': 'НДС 10/110'},
                                                                              {'code': '20/120', 'name': 'НДС 20/120'}])

    @allure.description("Получение актуального списка возможных статусов заказа СД Почта России")
    def test_info_statuses(self, app, token):
        result_info_delivery_service_services = app.info.info_delivery_service_services(code="RussianPost",
                                                                                        headers=token)
        Checking.check_status_code(response=result_info_delivery_service_services, expected_status_code=200)
        Checking.checking_json_key(response=result_info_delivery_service_services, expected_value=[
            {'name': 'no-return', 'title': 'Возврату не подлежит', 'description': 'Возврату не подлежит'},
            {'name': 'open', 'title': 'Можно вскрывать до получения оплаты с клиента',
             'description': 'Можно вскрывать до получения оплаты с клиента'},
            {'name': 'pay-by-card', 'title': 'COD (картой или наличными)', 'description': 'COD (картой или наличными)'},
            {'name': 'sms', 'title': 'SMS информирование', 'description': 'SMS уведомление получателя'}])

    @allure.description("Получение оферов по Почте России (Courier)")
    @pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
    def test_offers_courier(self, app, payment_type, token):
        # Todo проработать вопрос с WIDGET OFFERS
        shop_id = app.shop.get_shops_id(headers=token)
        warehouse_id = app.warehouse.get_warehouses_id(headers=token)
        result_offers_courier = app.offers.get_offers(warehouse_id=warehouse_id[0], shop_id=shop_id[0],
                                                      payment_type=payment_type, types="Courier",
                                                      delivery_service_code="RussianPost", headers=token)
        Checking.check_status_code(response=result_offers_courier, expected_status_code=200)
        Checking.checking_json_key(response=result_offers_courier, expected_value=['Courier'])

    @allure.description("Получение оферов по Почте России (DeliveryPoint)")
    @pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
    def test_offers_delivery_point(self, app, payment_type, token):
        shop_id = app.shop.get_shops_id(headers=token)
        warehouse_id = app.warehouse.get_warehouses_id(headers=token)
        result_offers_delivery_point = app.offers.get_offers(warehouse_id=warehouse_id[0], shop_id=shop_id[0],
                                                             payment_type=payment_type, types="DeliveryPoint",
                                                             delivery_service_code="RussianPost", headers=token)
        Checking.check_status_code(response=result_offers_delivery_point, expected_status_code=200)
        Checking.checking_json_key(response=result_offers_delivery_point, expected_value=['PostOffice'])

    @allure.description("Получение оферов по Почте России (PostOffice)")
    @pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
    def test_offers_russian_post(self, app, payment_type, token):
        shop_id = app.shop.get_shops_id(headers=token)
        warehouse_id = app.warehouse.get_warehouses_id(headers=token)
        result_offers_delivery_point = app.offers.get_offers(warehouse_id=warehouse_id[0], shop_id=shop_id[0],
                                                             payment_type=payment_type, types="PostOffice",
                                                             delivery_service_code="RussianPost", headers=token)
        Checking.check_status_code(response=result_offers_delivery_point, expected_status_code=200)
        Checking.checking_json_key(response=result_offers_delivery_point, expected_value=['PostOffice'])

    @allure.description("Создание Courier заказа по Почте России")
    def test_create_order_russian_post_courier(self, app, token):
        shop_id = app.shop.get_shops_id(headers=token)
        warehouse_id = app.warehouse.get_warehouses_id(headers=token)
        result_order = app.order.create_order(warehouse_id=warehouse_id[0], shop_id=shop_id[0], payment_type="Paid",
                                              type_ds="Courier", service="RussianPost", tariff="24", price=1000,
                                              declared_value=1500, headers=token)
        Checking.check_status_code(response=result_order, expected_status_code=201)
        Checking.checking_json_key(response=result_order, expected_value=['id', 'type', 'url', 'status'])
        result_get_order_by_id = app.order.get_order_by_id(order_id=result_order.json()["id"], headers=token)
        Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
        Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")

    @allure.description("Создание DeliveryPoint заказа по Почте России")
    def test_create_order_russian_post_delivery_point(self, app, token):
        shop_id = app.shop.get_shops_id(headers=token)
        warehouse_id = app.warehouse.get_warehouses_id(headers=token)
        result_order = app.order.create_order(warehouse_id=warehouse_id[0], shop_id=shop_id[0], payment_type="Paid",
                                              length=15, width=15, height=15, type_ds="DeliveryPoint",
                                              service="RussianPost", tariff="23", delivery_point_code="914841",
                                              price=1000, declared_value=1500, headers=token)
        Checking.check_status_code(response=result_order, expected_status_code=201)
        Checking.checking_json_key(response=result_order, expected_value=['id', 'type', 'url', 'status'])
        result_get_order_by_id = app.order.get_order_by_id(order_id=result_order.json()["id"], headers=token)
        Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")

    @allure.description("Создание PostOffice заказа по Почте России")
    @pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
    def test_create_order_russian_post_post_office(self, app, payment_type, token):
        shop_id = app.shop.get_shops_id(headers=token)
        warehouse_id = app.warehouse.get_warehouses_id(headers=token)
        result_order = app.order.create_order(warehouse_id=warehouse_id[0], shop_id=shop_id[0],
                                              payment_type=payment_type, type_ds="PostOffice", service="RussianPost",
                                              tariff=choice(["23", "47", "4", "7"]), price=1000, declared_value=1500,
                                              headers=token)
        Checking.check_status_code(response=result_order, expected_status_code=201)
        Checking.checking_json_key(response=result_order, expected_value=['id', 'type', 'url', 'status'])
        result_get_order_by_id = app.order.get_order_by_id(order_id=result_order.json()["id"], headers=token)
        Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
        Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")

    @allure.description("Попытка получения этикетки Почты России вне партии")
    def test_get_label_russian_post_out_of_parcel(self, app, token):
        list_order_id = app.order.get_orders_id(headers=token)
        for order_id in list_order_id:
            result_label = app.document.get_label(order_id=order_id, headers=token)
            Checking.check_status_code(response=result_label, expected_status_code=404)

    @allure.description("Редактирование заказа")
    def test_editing_order(self, app, token):
        order_list_id = app.order.get_orders_id(headers=token)
        random_order = choice(order_list_id)
        result_order_put = app.order.update_order(order_id=random_order, weight=5, length=12, width=14, height=11,
                                                  declared_value=2500, family_name="Иванов", headers=token)
        Checking.check_status_code(response=result_order_put, expected_status_code=200)
        Checking.checking_big_json(response=result_order_put, key_name="weight", expected_value=5)
        Checking.checking_big_json(response=result_order_put, key_name="payment", field="declaredValue",
                                   expected_value=2500)
        Checking.checking_big_json(response=result_order_put, key_name="dimension", field="length", expected_value=12)
        Checking.checking_big_json(response=result_order_put, key_name="dimension", field="width", expected_value=14)
        Checking.checking_big_json(response=result_order_put, key_name="dimension", field="height", expected_value=11)
        Checking.checking_big_json(response=result_order_put, key_name="recipient", field="familyName",
                                   expected_value="Иванов")

    @allure.description("Получение информации об истории изменения статусов заказа")
    def test_order_status(self, app, token):
        order_list_id = app.order.get_orders_id(headers=token)
        for order_id in order_list_id:
            result_order_status = app.order.get_order_statuses(order_id=order_id, headers=token)
            Checking.check_status_code(response=result_order_status, expected_status_code=200)
            Checking.checking_in_list_json_value(response=result_order_status, key_name="status",
                                                 expected_value="created")

    @allure.description("Получение подробной информации о заказе")
    def test_order_details(self, app, token):
        order_list_id = app.order.get_orders_id(headers=token)
        for order_id in order_list_id:
            result_order_details = app.order.get_order_details(order_id=order_id, headers=token)
            Checking.check_status_code(response=result_order_details, expected_status_code=200)
            Checking.checking_json_key(response=result_order_details, expected_value=['returnItems', 'returnReason',
                                                                                      'delayReason', 'paymentType',
                                                                                      'pickupDate',
                                                                                      'declaredDeliveryDate',
                                                                                      'storageDateEnd'])

    @allure.description("Создание партии")
    def test_create_parcel(self, app, token):
        orders_id = app.order.get_orders_id(headers=token)
        result_create_parcel = app.parcel.create_parcel(order_id=choice(orders_id), headers=token)
        Checking.check_status_code(response=result_create_parcel, expected_status_code=207)
        Checking.checking_in_list_json_value(response=result_create_parcel, key_name="type", expected_value="Parcel")

    @allure.description("Редактирование партии(Добавление заказов)")
    def test_add_order_in_parcel(self, app, token):
        parcel_id = app.parcel.get_parcels_id(headers=token)
        orders_id = app.order.get_orders_id(headers=token)
        for order in orders_id:
            old_list_order_in_parcel = app.parcel.get_order_in_parcel(parcel_id=parcel_id[0], headers=token)
            result_parcel_add = app.parcel.change_parcel_orders(order_id=order, parcel_id=parcel_id[0], op="add",
                                                                headers=token)
            Checking.check_status_code(response=result_parcel_add, expected_status_code=200)
            new_list_order_in_parcel = app.parcel.get_order_in_parcel(parcel_id=parcel_id[0], headers=token)
            Checking.checking_sum_len_lists(old_list=old_list_order_in_parcel, new_list=new_list_order_in_parcel)

    @allure.description("Редактирование партии(Изменение даты отправки партии)")
    def test_change_shipment_date(self, app, token):
        parcel_id = app.parcel.get_parcels_id(headers=token)
        result_shipment_date = app.parcel.change_parcel_shipment_date(parcel_id=parcel_id[0], day=5, headers=token)
        Checking.check_status_code(response=result_shipment_date, expected_status_code=200)
        new_date = result_shipment_date.json()["data"]["request"]["shipmentDate"]
        Checking.check_date_change(calendar_date=new_date, number_of_days=5)

    @allure.description("Получение этикетки")
    def test_create_label(self, app, token):
        parcel_id = app.parcel.get_parcels_id(headers=token)
        result_order_in_parcel = app.parcel.get_order_in_parcel(parcel_id=parcel_id[0], headers=token)
        for order_id in result_order_in_parcel:
            result_label = app.document.get_label(order_id=order_id, headers=token)
            Checking.check_status_code(response=result_label, expected_status_code=200)

    @allure.description("Получение АПП")
    def test_create_app(self, app, token):
        parcel_id = app.parcel.get_parcels_id(headers=token)
        result_app = app.document.get_app(parcel_id=parcel_id[0], headers=token)
        Checking.check_status_code(response=result_app, expected_status_code=200)

    @allure.description("Получение документов")
    def test_create_documents(self, app, token):
        parcel_id = app.parcel.get_parcels_id(headers=token)
        result_documents = app.document.get_documents(parcel_id=parcel_id[0], headers=token)
        Checking.check_status_code(response=result_documents, expected_status_code=200)

    @allure.description("Редактирование партии(Удаление заказа)")
    def test_remove_order_in_parcel(self, app, token):
        parcel_id = app.parcel.get_parcels_id(headers=token)
        old_list_order = app.parcel.get_order_in_parcel(parcel_id=parcel_id[0], headers=token)
        result_order_in_parcel = app.parcel.get_order_in_parcel(parcel_id=parcel_id[0], headers=token)
        result_parcel_remove = app.parcel.change_parcel_orders(order_id=choice(result_order_in_parcel),
                                                               parcel_id=parcel_id[0], op="remove", headers=token)
        new_list_order = app.parcel.get_order_in_parcel(parcel_id=parcel_id[0], headers=token)
        Checking.check_status_code(response=result_parcel_remove, expected_status_code=200)
        Checking.checking_difference_len_lists(old_list=old_list_order, new_list=new_list_order)

    @allure.description("Удаление заказа")
    def test_delete_order(self, app, token):
        orders_id_list = app.order.get_orders_id(headers=token)
        random_order_id = choice(orders_id_list)
        result_delete_order = app.order.delete_order(order_id=random_order_id, headers=token)
        Checking.check_status_code(response=result_delete_order, expected_status_code=204)
        result_get_order_by_id = app.order.get_order_by_id(order_id=random_order_id, headers=token)
        Checking.check_status_code(response=result_get_order_by_id, expected_status_code=404)
