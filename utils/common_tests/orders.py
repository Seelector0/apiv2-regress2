from random import choice, randrange
from utils.global_enums import INFO
from utils.checking import Checking
import pytest


class CommonOrders:

    @staticmethod
    def test_single_order_common(app, shop_id, warehouse_id, payment_type, delivery_type,
                                 connections, shared_data, service, tariff=None, shared_data_order_type=None,
                                 declared_value=1000, **kwargs):
        """Создание одноместного заказа"""
        new_order = app.order.post_single_order(shop_id=shop_id, warehouse_id=warehouse_id,
                                                payment_type=payment_type, type_ds=delivery_type, service=service,
                                                tariff=tariff, declared_value=declared_value, **kwargs)
        Checking.check_status_code(response=new_order, expected_status_code=201)
        Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
        order_id = new_order.json()["id"]
        connections.wait_create_order(order_id=order_id)
        Checking.check_value_comparison(responses={"POST v2/order/{id}": new_order},
                                        one_value=connections.get_list_order_value(order_id=order_id,
                                                                                   value="status"),
                                        two_value=["created"])
        shared_data.append(order_id)
        if shared_data_order_type is not None:
            shared_data_order_type.append(order_id)

    @staticmethod
    def test_multi_order_common(app, shop_id, warehouse_id, payment_type, delivery_type, service, connections,
                                shared_data, tariff=None, delivery_point_code=None, declared_value=500, **kwargs):
        """Создание многоместного заказа"""
        barcode_1 = kwargs.pop('barcode_1', f"{randrange(1000000, 9999999)}")
        barcode_2 = kwargs.pop('barcode_2', f"{randrange(1000000, 9999999)}")
        new_order = app.order.post_multi_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                               type_ds=delivery_type, service=service,
                                               delivery_point_code=delivery_point_code,
                                               tariff=tariff, declared_value=declared_value,
                                               barcode_1=barcode_1,
                                               barcode_2=barcode_2, **kwargs)
        Checking.check_status_code(response=new_order, expected_status_code=201)
        Checking.checking_json_key(response=new_order, expected_value=INFO.created_entity)
        order_id = new_order.json()["id"]
        connections.wait_create_order(order_id=order_id)
        Checking.check_value_comparison(responses={"POST v2/order/{id}": new_order},
                                        one_value=connections.get_list_order_value(order_id=order_id,
                                                                                   value="status"),
                                        two_value=["created"])
        shared_data.append(order_id)

    @staticmethod
    def test_create_order_from_file_common(app, shop_id, warehouse_id, file_extension, connections, code=None,
                                           shared_data=None):
        """Создание заказа из файла"""
        if code is not None:
            new_orders = app.order.post_import_order_format_metaship(shop_id=shop_id, warehouse_id=warehouse_id,
                                                                     code=code, file_extension=file_extension)
        else:
            new_orders = app.order.post_import_order_format_russian_post(shop_id=shop_id, warehouse_id=warehouse_id,
                                                                         file_extension=file_extension)

        Checking.check_status_code(response=new_orders, expected_status_code=200)
        for order in new_orders.json().values():
            order_id = order["id"]
            connections.wait_create_order(order_id=order_id)
            Checking.check_value_comparison(responses={"POST v2/import/orders": new_orders},
                                            one_value=connections.get_list_order_value(order_id=order_id,
                                                                                       value="status"),
                                            two_value=["created"])
            shared_data.append(order_id)

    @staticmethod
    def test_editing_order_common(app, shared_data, delivery_service=None):
        """Редактирование заказа"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        random_order = choice(shared_data)
        order_put = app.order.put_order(order_id=random_order, delivery_service=delivery_service, weight=5, length=12,
                                        width=14, height=11, family_name="Иванов", first_name="Петр",
                                        second_name="Сергеевич", phone_number="+79097859012", email="new_test@mail.ru",
                                        address="119634 ул. Лукинская, дом 1, кв. 1", comment="Всё зашибись.")
        Checking.check_status_code(response=order_put, expected_status_code=200)
        Checking.checking_big_json(response=order_put, key_name="weight", expected_value=5)
        Checking.checking_big_json(response=order_put, key_name="dimension", field="length", expected_value=12)
        Checking.checking_big_json(response=order_put, key_name="dimension", field="width", expected_value=14)
        Checking.checking_big_json(response=order_put, key_name="dimension", field="height", expected_value=11)
        Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName",
                                   expected_value="Иванов")
        Checking.checking_big_json(response=order_put, key_name="recipient", field="firstName", expected_value="Петр")
        Checking.checking_big_json(response=order_put, key_name="recipient", field="secondName",
                                   expected_value="Сергеевич")
        Checking.checking_big_json(response=order_put, key_name="recipient", field="phoneNumber",
                                   expected_value="+79097859012")
        Checking.checking_big_json(response=order_put, key_name="recipient", field="email",
                                   expected_value="new_test@mail.ru")
        Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName",
                                   expected_value="Иванов")
        Checking.checking_big_json(response=order_put, key_name="recipient", field="address",
                                   expected_value={
                                       "raw": "119634 ул. Лукинская, дом 1, кв. 1",
                                       "countryCode": None
                                   })

    @staticmethod
    def test_patch_single_order_common(app, delivery_service, connections, shared_data):
        """Редактирование одноместного заказа"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        patch_single_order = None
        order_id = shared_data.pop()
        single_order = app.order.get_order_id(order_id=order_id)
        items = single_order.json()["data"]["request"]["places"][0]["items"]
        Checking.check_status_code(response=single_order, expected_status_code=200)
        if delivery_service == "Cdek":
            patch_single_order = app.order.patch_order_items_cdek(order_id=order_id, name_1="Бамбук", name_2="Книга")
            Checking.check_status_code(response=patch_single_order, expected_status_code=200)
        elif delivery_service == "FivePost":
            patch_single_order = app.order.patch_order_items_five_post(order_id=order_id, items_name="семена бамбука")
            Checking.check_status_code(response=patch_single_order, expected_status_code=200)
        elif delivery_service == "TopDelivery":
            patch_single_order = app.order.patch_create_multy_order(order_id=order_id, items=items)
            Checking.check_status_code(response=patch_single_order, expected_status_code=200)
        connections.wait_create_order(order_id=order_id)
        order_by_id = app.order.get_order_id(order_id=order_id)
        Checking.check_status_code(response=order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=order_by_id, key_name="status", expected_value="created")
        assert_order_patch = app.order.get_order_patches(order_id=patch_single_order.json()["id"])
        Checking.check_status_code(response=assert_order_patch, expected_status_code=200)
        if delivery_service == "Cdek":
            Checking.check_value_comparison(responses={"PATCH v2/order/{id}": patch_single_order,
                                                       "GET v2/order/{id} created": single_order,
                                                       "GET v2/order/{id} patched": order_by_id},
                                            one_value=len(single_order.json()["data"]["request"]["places"]),
                                            two_value=1)
            Checking.check_value_comparison(responses={"PATCH v2/order/{id}": patch_single_order,
                                                       "GET v2/order/{id} created": single_order,
                                                       "GET v2/order/{id} patched": order_by_id},
                                            one_value=len(order_by_id.json()["data"]["request"]["places"]), two_value=2)
        elif delivery_service == "FivePost":
            field = order_by_id.json()["data"]["request"]["places"][0]["items"][0]
            Checking.check_value_comparison(responses={"PATCH v2/order/{id}": patch_single_order,
                                                       "GET v2/order/{id} created": single_order,
                                                       "GET v2/order/{id} patched": order_by_id},
                                            one_value=field["name"],
                                            two_value="семена бамбука")
        elif delivery_service == "TopDelivery":
            Checking.check_value_comparison(responses={"PATCH v2/order/{id}": patch_single_order,
                                                       "GET v2/order/{id} created": single_order,
                                                       "GET v2/order/{id} patched": order_by_id},
                                            one_value=len(single_order.json()["data"]["request"]["places"]),
                                            two_value=1)
            Checking.check_value_comparison(responses={"PATCH v2/order/{id}": patch_single_order,
                                                       "GET v2/order/{id} created": single_order,
                                                       "GET v2/order/{id} patched": order_by_id},
                                            one_value=len(patch_single_order.json()["data"]["request"]["places"]),
                                            two_value=3)

    @staticmethod
    def test_patch_add_single_order_from_multi_order_common(app, connections, shared_data):
        """Создание одноместного заказа из многоместного"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        order_id = choice(shared_data)
        multi_order = app.order.get_order_id(order_id=order_id)
        Checking.check_status_code(response=multi_order, expected_status_code=200)
        patch_multi_order = app.order.patch_order(order_id=order_id, name="Пуфик", price=500, count=2, weight=2,
                                                  barcode=f"{randrange(1000000, 9999999)}")
        Checking.check_status_code(response=patch_multi_order, expected_status_code=200)
        connections.wait_create_order(order_id=order_id)
        Checking.checking_json_value(response=patch_multi_order, key_name="status", expected_value="created")
        assert len(multi_order.json()["data"]["request"]["places"]) > \
               len(patch_multi_order.json()["data"]["request"]["places"])

    @staticmethod
    def test_patch_multi_order_common(app, connections, shared_data, delivery_service=None):
        """Добавление items в многоместный заказ"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        order_id = choice(shared_data)
        old_len_order_list, patch_order = app.order.patch_order_add_item(order_id=order_id)
        Checking.check_status_code(response=patch_order, expected_status_code=200)
        Checking.checking_json_value(response=patch_order, key_name="status", expected_value="created")
        if delivery_service == "Cdek":
            Checking.checking_json_value(response=patch_order, key_name="state",
                                         expected_value="editing-external-processing")
        else:
            Checking.checking_json_value(response=patch_order, key_name="state", expected_value="succeeded")
        connections.wait_create_order(order_id=order_id)
        new_len_order_list = app.order.get_order_id(order_id=order_id)
        Checking.check_status_code(response=new_len_order_list, expected_status_code=200)
        Checking.checking_json_value(response=new_len_order_list, key_name="status", expected_value="created")
        Checking.checking_sum_len_lists(responses={"PATCH v2/order/{id}": patch_order,
                                                   "GET v2/order/{id} created": old_len_order_list,
                                                   "GET v2/order/{id} patched": new_len_order_list},
                                        old_list=old_len_order_list.json()["data"]["request"]["places"],
                                        new_list=new_len_order_list.json()["data"]["request"]["places"])

    @staticmethod
    def test_editing_order_place_common(app, connections, shared_data):
        """Редактирование грузомест"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        order_id = shared_data.pop()
        patch_order = app.order.patch_order(order_id=order_id, name="Пуфик", price=500, count=2, weight=2)
        Checking.check_status_code(response=patch_order, expected_status_code=200)
        connections.wait_create_order(order_id=order_id)
        order_by_id = app.order.get_order_id(order_id=order_id)
        Checking.check_status_code(response=order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=order_by_id, key_name="status", expected_value="created")
        field = order_by_id.json()["data"]["request"]["places"][0]["items"][0]
        Checking.check_value_comparison(responses={"PATCH v2/order/{id}": patch_order},
                                        one_value=field["name"], two_value="Пуфик")
        Checking.check_value_comparison(responses={"PATCH v2/order/{id}": patch_order},
                                        one_value=field["price"], two_value=500)
        Checking.check_value_comparison(responses={"PATCH v2/order/{id}": patch_order},
                                        one_value=field["count"], two_value=2)
        Checking.check_value_comparison(responses={"PATCH v2/order/{id}": patch_order},
                                        one_value=field["weight"], two_value=2)

    @staticmethod
    def patch_order_recipient_common(app, connections, shared_data, **kwargs):
        """Редактирование информации о получателе в заказе"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        order_id = shared_data.pop()
        order_patch = app.order.patch_order_recipient(order_id=order_id, phone_number="+79266967503",
                                                      email="new_test_email@bk.ru", **kwargs)
        Checking.check_status_code(response=order_patch, expected_status_code=200)
        connections.wait_create_order(order_id=order_patch.json()["id"])
        assert_order_patch = app.order.get_order_patches(order_id=order_patch.json()["id"])
        Checking.check_status_code(response=assert_order_patch, expected_status_code=200)
        Checking.checking_in_list_json_value(response=assert_order_patch, key_name="state", expected_value="succeeded")
        order_by_id = app.order.get_order_id(order_id=order_id)
        Checking.check_status_code(response=order_by_id, expected_status_code=200)
        Checking.checking_big_json(response=order_by_id, key_name="recipient", field="email",
                                   expected_value="new_test_email@bk.ru")
        Checking.checking_big_json(response=order_by_id, key_name="recipient", field="phoneNumber",
                                   expected_value="+79266967503")
        if "family_name" in kwargs:
            Checking.checking_big_json(response=order_by_id, key_name="recipient", field="familyName",
                                       expected_value=kwargs["family_name"])
        if "first_name" in kwargs:
            Checking.checking_big_json(response=order_by_id, key_name="recipient", field="firstName",
                                       expected_value=kwargs["first_name"])
        if "second_name" in kwargs:
            Checking.checking_big_json(response=order_by_id, key_name="recipient", field="secondName",
                                       expected_value=kwargs["second_name"])
        if "address" in kwargs:
            Checking.checking_big_json(response=order_by_id, key_name="recipient", field="address",
                                       expected_value=kwargs["address"])

    @staticmethod
    def test_patch_order_weight_common(app, connections, shared_data):
        """Редактирование веса в заказе"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        order_id = shared_data.pop()
        order_patch = app.order.patch_order_weight(order_id=order_id, weight=4)
        Checking.check_status_code(response=order_patch, expected_status_code=200)
        connections.wait_create_order(order_id=order_id)
        get_order_by_id = app.order.get_order_id(order_id=order_patch.json()["id"])
        Checking.checking_big_json(response=get_order_by_id, key_name="weight", expected_value=4)

    @staticmethod
    def test_get_orders_common(app):
        """Получение списка заказов"""
        list_orders = app.order.get_orders()
        Checking.check_status_code(response=list_orders, expected_status_code=200)
        Checking.check_response_is_not_empty(response=list_orders)

    @staticmethod
    def test_get_order_by_id_common(app, shared_data):
        """Получение информации о заказе"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        order_id = app.order.get_order_id(order_id=choice(shared_data))
        Checking.check_status_code(response=order_id, expected_status_code=200)
        Checking.checking_json_key(response=order_id, expected_value=INFO.entity_order)

    @staticmethod
    def test_order_details_common(app, shared_data):
        """Получение подробной информации о заказе"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        order_id = choice(shared_data)
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.checking_json_key(response=order_details, expected_value=INFO.details)

    @staticmethod
    def test_order_status_common(app, shared_data):
        """Получение информации об истории изменения статусов заказа"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        order_id = choice(shared_data)
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.checking_in_list_json_value(response=order_status, key_name="status", expected_value="created")

    @staticmethod
    def test_get_labels_out_of_parcel_common(app, shared_data, labels=None, format_=None):
        """Получения этикеток вне партии"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        order_id = choice(shared_data)
        if labels:
            label = app.document.get_label(order_id=order_id, type_=labels)
        elif format_:
            label = app.document.get_label(order_id=order_id, size_format=format_)
        else:
            label = app.document.get_label(order_id=order_id)
        Checking.check_status_code(response=label, expected_status_code=200)

    @staticmethod
    def test_generate_security_common(app, shared_data):
        """Получение кода выдачи заказа"""
        if not shared_data:
            pytest.fail("Список заказов 'shared_data' пуст, невозможно выполнить тест.")
        order_id = choice(shared_data)
        security_code = app.order.get_generate_security_code(order_id=order_id)
        Checking.check_status_code(response=security_code, expected_status_code=200)
        Checking.checking_json_key(response=security_code, expected_value=["code"])

    @staticmethod
    def test_delete_order_common(app, connections, shared_data, delivery_service=None):
        """Удаление заказа"""
        if not shared_data.get("order_ids"):
            pytest.fail("Список заказов 'order_ids' пуст, невозможно выполнить тест.")
        random_order_id = shared_data["order_ids"].pop()
        delete_order = app.order.delete_order(order_id=random_order_id)
        Checking.check_status_code(response=delete_order, expected_status_code=204)
        Checking.check_value_comparison(responses={"DELETE v2/order/{id}": delete_order},
                                        one_value=connections.get_list_order_value(order_id=random_order_id,
                                                                                   value="deleted"),
                                        two_value=[True])
        if delivery_service == "RussianPost":
            lists_to_check = ["orders_courier", "orders_delivery_point", "orders_post_office", "orders_terminal"]
            for list_name in lists_to_check:
                if random_order_id in shared_data[list_name]:
                    shared_data[list_name].remove(random_order_id)

    @staticmethod
    def test_create_intake_common(app, shop_id, warehouse_id, delivery_service, connections):
        """Создание забора"""
        new_intake = app.intakes.post_intakes(shop_id=shop_id, warehouse_id=warehouse_id,
                                              delivery_service=delivery_service)
        Checking.check_status_code(response=new_intake, expected_status_code=201)
        Checking.checking_json_key(response=new_intake, expected_value=INFO.created_entity)
        status = connections.get_list_intakes_value(intake_id=new_intake.json()["id"], value="status")
        if delivery_service == "Cdek":
            expected_status = ["pending"]
        else:
            expected_status = ["created"]
        Checking.check_value_comparison(responses={"POST v2/intakes": new_intake},
                                        one_value=status, two_value=expected_status)
