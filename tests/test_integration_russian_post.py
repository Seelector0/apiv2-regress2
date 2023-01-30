from utils.checking import Checking
from random import choice
import pytest
import allure


@allure.epic("Тесты Почты России по Интеграции")
class TestRussianPostIntegration:


    @allure.description("Создание магазина")
    def test_create_integration_shop(self, app, token):
        global result_new_shop
        result_new_shop = app.shop.create_shop(headers=token)
        Checking.check_status_code(response=result_new_shop, expected_status_code=201)
        Checking.checking_json_key(response=result_new_shop, expected_value=['id', 'type', 'url', 'status'])


    @allure.description("Создание склада")
    def test_create_new_warehouse(self, app, token):
        global result_new_warehouse
        result_new_warehouse = app.warehouse.create_warehouse(fullname="Виктор Викторович", headers=token)
        Checking.check_status_code(response=result_new_warehouse, expected_status_code=201)
        Checking.checking_json_key(response=result_new_warehouse, expected_value=['id', 'type', 'url', 'status'])


    @allure.description("Подключение настроек Почты России")
    def test_integration_russian_post(self, app, token):
        result_russian_post = app.service.delivery_services_russian_post(connection_type="integration",
                                                                         shop_id=result_new_shop.json()["id"],
                                                                         headers=token)
        Checking.check_status_code(response=result_russian_post, expected_status_code=201)
        Checking.checking_json_key(response=result_russian_post, expected_value=['id', 'type', 'url', 'status'])


    @allure.description("Получение оферов по Почте России")
    @pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
    @pytest.mark.parametrize("types", ["Courier", "DeliveryPoint","PostOffice"])
    def test_offers(self, app, payment_type, types, token):
        # Todo проработать вопрос с WIDGET OFFERS
        result_offers = app.offers.get_offers(warehouse_id=result_new_warehouse.json()["id"],
                                              shop_id=result_new_shop.json()["id"],
                                              payment_type=payment_type, types=types, delivery_service_code="RussianPost",
                                              headers=token)
        Checking.check_status_code(response=result_offers, expected_status_code=200)


    @allure.description("Создание Courier заказа по Почте России")
    def test_create_order_russian_post_courier(self, app, token):
        result_order = app.order.create_order(warehouse_id=result_new_warehouse.json()["id"],
                                              shop_id=result_new_shop.json()["id"], payment_type="Paid",
                                              type_ds="Courier", service="RussianPost",
                                              tariff="24",price=1000, declared_value=1500, headers=token)
        Checking.check_status_code(response=result_order, expected_status_code=201)
        Checking.checking_json_key(response=result_order, expected_value=['id', 'type', 'url', 'status'])
        result_get_order_by_id = app.order.get_order_by_id(order_id=result_order.json()["id"], headers=token)
        Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
        Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


    @allure.description("Создание DeliveryPoint заказа по Почте России")
    def test_create_order_russian_post_delivery_point(self, app,token):
        result_order = app.order.create_order(warehouse_id=result_new_warehouse.json()["id"],
                                              shop_id=result_new_shop.json()["id"], payment_type="Paid", length=15,
                                              width=15, height=15, type_ds="DeliveryPoint", service="RussianPost",
                                              tariff="23", delivery_point_code="914841", price=1000,
                                              declared_value=1500, headers=token)
        Checking.check_status_code(response=result_order, expected_status_code=201)
        Checking.checking_json_key(response=result_order, expected_value=['id', 'type', 'url', 'status'])
        result_get_order_by_id = app.order.get_order_by_id(order_id=result_order.json()["id"], headers=token)
        Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")


    @allure.description("Создание PostOffice заказа по Почте России")
    @pytest.mark.parametrize("payment_type", ["Paid", "PayOnDelivery"])
    def test_create_order_russian_post_post_office(self, app, payment_type, token):
        result_order = app.order.create_order(warehouse_id=result_new_warehouse.json()["id"],
                                              shop_id=result_new_shop.json()["id"], payment_type=payment_type,
                                              type_ds="PostOffice", service="RussianPost",
                                              tariff=choice(["23", "47", "4", "7"]), price=1000,
                                              declared_value=1500, headers=token)
        Checking.check_status_code(response=result_order, expected_status_code=201)
        Checking.checking_json_key(response=result_order, expected_value=['id', 'type', 'url', 'status'])
        result_get_order_by_id = app.order.get_order_by_id(order_id=result_order.json()["id"], headers=token)
        Checking.check_status_code(response=result_get_order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=result_get_order_by_id, key_name="status", expected_value="created")
        Checking.checking_json_value(response=result_get_order_by_id, key_name="state", expected_value="succeeded")


    @allure.description("Получение информации об истории изменения статусов заказа")
    def test_order_status(self, app, token):
        order_list_id = app.order.get_orders_id(headers=token)
        for order_id in order_list_id:
            result_order_status = app.order.get_order_statuses(order_id=order_id, headers=token)
            Checking.check_status_code(response=result_order_status, expected_status_code=200)
            Checking.checking_in_list_json_value(response=result_order_status, key_name="status", expected_value="created")


    @allure.description("Получение подробной информации о заказе")
    def test_order_details(self, app, token):
        order_list_id = app.order.get_orders_id(headers=token)
        for order_id in order_list_id:
            result_order_details = app.order.get_order_details(order_id=order_id, headers=token)
            Checking.check_status_code(response=result_order_details, expected_status_code=200)
            Checking.checking_json_key(response=result_order_details, expected_value=[
                'returnItems', 'returnReason', 'delayReason', 'paymentType',
                'pickupDate', 'declaredDeliveryDate', 'storageDateEnd'])


    @allure.description("Создание партии")
    def test_create_parcel(self, app, token):
        global result_create_parcel
        orders_id = app.order.get_orders_id(headers=token)
        result_create_parcel = app.parcel.create_parcel(order_id=choice(orders_id), headers=token)
        Checking.check_status_code(response=result_create_parcel, expected_status_code=207)
        Checking.checking_in_list_json_value(response=result_create_parcel, key_name="type", expected_value="Parcel")


    @allure.description("Редактирование партии(Добавление заказов)")
    def test_add_order_in_parcel(self, app, token):
        orders_id = app.order.get_orders_id(headers=token)
        for order in orders_id:
            result_parcel_add = app.parcel.change_parcel_orders(order_id=order,
                                                                parcel_id=result_create_parcel.json()[0]["id"],
                                                                op="add", headers=token)
            Checking.check_status_code(response=result_parcel_add, expected_status_code=200)


    @allure.description("Редактирование партии(Изменение даты отправки партии)")
    def test_change_shipment_date(self, app, token):
        result_parcel_list = app.parcel.get_parcel_id(headers=token)
        for parcel_id in result_parcel_list:
            result_shipment_date = app.parcel.change_parcel_shipment_date(parcel_id=parcel_id, day=5, headers=token)
            Checking.check_status_code(response=result_shipment_date, expected_status_code=200)
            new_date = result_shipment_date.json()["data"]["request"]["shipmentDate"]
            Checking.check_date_change(calendar_date=new_date, number_of_days=5)


    @allure.description("Получение этикетки")
    def test_label_download(self, app, token):
        result_order_in_parcel = app.parcel.get_order_in_parcel(parcel_id=result_create_parcel.json()[0]["id"],
                                                                headers=token)
        for order_id in result_order_in_parcel:
            Checking.download_file_false(directory=app.download_directory, file=f"Этикетки-Почта_России-{order_id}.pdf")
            result_label = app.document.get_label(order_id=order_id, headers=token)
            Checking.check_status_code(response=result_label, expected_status_code=200)
            app.download_file(name="Этикетки-Почта_России", value_id=order_id, expansion="pdf", response=result_label)
            Checking.download_file_true(directory=app.download_directory, file=f"Этикетки-Почта_России-{order_id}.pdf")


    @allure.description("Получение АПП")
    def test_app_download(self, app, token):
        result_parcel_list = app.parcel.get_parcel_id(headers=token)
        for parcel_id in result_parcel_list:
            Checking.download_file_false(directory=app.download_directory, file=f"Акт-{parcel_id}.pdf")
            result_app = app.document.get_app(parcel_id=parcel_id, headers=token)
            Checking.check_status_code(response=result_app, expected_status_code=200)
            app.download_file(name="Акт", value_id=parcel_id, expansion="pdf", response=result_app)
            Checking.download_file_true(directory=app.download_directory, file=f"Акт-{parcel_id}.pdf")


    @allure.description("Получение документов")
    def test_documents_download(self, app, token):
        result_parcel_list = app.parcel.get_parcel_id(headers=token)
        for parcel_id in result_parcel_list:
            Checking.download_file_false(directory=app.download_directory, file=f"Документы-{parcel_id}.zip")
            result_documents = app.document.get_documents(parcel_id=parcel_id, headers=token)
            Checking.check_status_code(response=result_documents, expected_status_code=200)
            app.download_file(name="Документы", value_id=parcel_id, expansion="zip", response=result_documents)
            Checking.download_file_true(directory=app.download_directory, file=f"Документы-{parcel_id}.zip")


    @allure.description("Редактирование партии(Удаление заказа)")
    def test_remove_order_in_parcel(self, app, token):
        # Todo Дописать проверки обязательных полей
        result_order_in_parcel = app.parcel.get_order_in_parcel(parcel_id=result_create_parcel.json()[0]["id"],
                                                                headers=token)
        result_parcel_remove = app.parcel.change_parcel_orders(order_id=choice(result_order_in_parcel),
                                                               parcel_id=result_create_parcel.json()[0]["id"],
                                                               op="remove", headers=token)
        Checking.check_status_code(response=result_parcel_remove, expected_status_code=200)


    @allure.description("Удаление заказа")
    def test_delete_order(self, app, token):
        orders_id_list = app.order.get_orders_id(headers=token)
        random_order_id = choice(orders_id_list)
        result_delete_order = app.order.delete_order(order_id=random_order_id, headers=token)
        Checking.check_status_code(response=result_delete_order, expected_status_code=204)
        result_get_order_by_id = app.order.get_order_by_id(order_id=random_order_id, headers=token)
        Checking.check_status_code(response=result_get_order_by_id, expected_status_code=404)
