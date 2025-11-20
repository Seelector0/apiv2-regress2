from utils.response_schemas import SCHEMAS
from utils.utils import check_shared_data
from random import choice, randrange
from utils.checking import Checking


class CommonOrders:

    @staticmethod
    def test_single_order_common(app, connections, shared_data=None, shared_data_order_type=None, **kwargs):
        """Создание одноместного заказа
        :param app: Объект приложения для работы с заказами через API.
        :param connections: Объект для взаимодействия с базой данных.
        :param shared_data: Общие тестовые данные, такие как идентификаторы заказов и магазинов.
        :param shared_data_order_type: Дополнительные данные о типе заказа (по умолчанию None).
        """
        link = kwargs.get("link")
        new_order = app.order.post_single_order(**kwargs)
        Checking.check_status_code(response=new_order, expected_status_code=201)
        if link:
            Checking.check_json_schema(response=new_order, schema=SCHEMAS.order.order_get_by_id_or_editing)
        else:
            Checking.check_json_schema(response=new_order, schema=SCHEMAS.order.order_create)
        order_id = new_order.json()["id"]
        connections.wait_create_order(order_id=order_id)
        Checking.check_value_comparison(responses={"POST v2/order/{id}": new_order},
                                        one_value=connections.get_list_order_value(order_id=order_id,
                                                                                   value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(responses={"POST v2/order/{id}": new_order},
                                        one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                                   value="state"),
                                        two_value=["succeeded"])
        if shared_data is not None:
            shared_data.append(order_id)
        if shared_data_order_type is not None:
            shared_data_order_type.append(order_id)

    @staticmethod
    def test_single_order_minimal_common(app, connections, shared_data=None, shared_data_order_type=None, **kwargs):
        """Создание одноместного заказа с минимальным набором атрибутов
        :param app: Объект приложения для работы с заказами через API.
        :param connections: Объект для взаимодействия с базой данных.
        :param shared_data: Общие тестовые данные, такие как идентификаторы заказов и магазинов.
        :param shared_data_order_type: Дополнительные данные о типе заказа (по умолчанию None).
        """
        link = kwargs.get("link")
        new_order = app.order.post_single_order_minimal(**kwargs)
        Checking.check_status_code(response=new_order, expected_status_code=201)
        if link:
            Checking.check_json_schema(response=new_order, schema=SCHEMAS.order.order_get_by_id_or_editing)
        else:
            Checking.check_json_schema(response=new_order, schema=SCHEMAS.order.order_create)
        order_id = new_order.json()["id"]
        connections.wait_create_order(order_id=order_id)
        Checking.check_value_comparison(responses={"POST v2/order/{id}": new_order},
                                        one_value=connections.get_list_order_value(order_id=order_id,
                                                                                   value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(responses={"POST v2/order/{id}": new_order},
                                        one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                                   value="state"),
                                        two_value=["succeeded"])
        if shared_data is not None:
            shared_data.append(order_id)
        if shared_data_order_type is not None:
            shared_data_order_type.append(order_id)

    @staticmethod
    def test_multi_order_common(app, connections, shared_data, **kwargs):
        """Создание многоместного заказа"""
        new_order = app.order.post_multi_order(**kwargs)
        Checking.check_status_code(response=new_order, expected_status_code=201)
        Checking.check_json_schema(response=new_order, schema=SCHEMAS.order.order_create)
        order_id = new_order.json()["id"]
        connections.wait_create_order(order_id=order_id)
        Checking.check_value_comparison(responses={"POST v2/order/{id}": new_order},
                                        one_value=connections.get_list_order_value(order_id=order_id,
                                                                                   value="status"),
                                        two_value=["created"])
        Checking.check_value_comparison(responses={"POST v2/order/{id}": new_order},
                                        one_value=connections.get_list_order_value(order_id=new_order.json()["id"],
                                                                                   value="state"),
                                        two_value=["succeeded"])
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
        Checking.check_json_schema(response=new_orders, schema=SCHEMAS.order.order_create_from_file)
        for order in new_orders.json().values():
            order_id = order["id"]
            connections.wait_create_order(order_id=order_id)
            Checking.check_value_comparison(responses={"POST v2/import/orders": new_orders},
                                            one_value=connections.get_list_order_value(order_id=order_id,
                                                                                       value="status"),
                                            two_value=["created"])
            Checking.check_value_comparison(responses={"POST v2/import/orders": new_orders},
                                            one_value=connections.get_list_order_value(order_id=order_id,
                                                                                       value="state"),
                                            two_value=["succeeded"])
            shared_data.append(order_id)

    @staticmethod
    def test_editing_order_common(app, shared_data, delivery_service=None):
        """Редактирование заказа"""
        check_shared_data(shared_data)
        order_id = choice(shared_data)
        try:
            order_put = app.order.put_order(order_id=order_id, delivery_service=delivery_service, weight=5, length=12,
                                            width=14, height=11, family_name="Иванов", first_name="Петр",
                                            second_name="Сергеевич", phone_number="+79097859012",
                                            email="new_test@mail.ru", address="119634 ул. Лукинская, дом 1, кв. 1",
                                            comment="Всё зашибись.")
            Checking.check_status_code(response=order_put, expected_status_code=200)
            Checking.check_json_schema(response=order_put, schema=SCHEMAS.order.order_get_by_id_or_editing)
            Checking.checking_big_json(response=order_put, key_name="weight", expected_value=5)
            if "dimension" in order_put and order_put["dimension"]:
                Checking.checking_big_json(response=order_put, key_name="dimension", field="length", expected_value=12)
                Checking.checking_big_json(response=order_put, key_name="dimension", field="width", expected_value=14)
                Checking.checking_big_json(response=order_put, key_name="dimension", field="height", expected_value=11)
            Checking.checking_big_json(response=order_put, key_name="recipient", field="familyName",
                                       expected_value="Иванов")
            Checking.checking_big_json(response=order_put, key_name="recipient", field="firstName",
                                       expected_value="Петр")
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
        except AssertionError:
            if order_id in shared_data:
                shared_data.remove(order_id)
            raise

    @staticmethod
    def test_patch_single_order_common(app, delivery_service, connections, shared_data):
        """Редактирование одноместного заказа"""
        check_shared_data(shared_data)
        patch_single_order = None
        order_id = shared_data.pop()
        single_order = app.order.get_order_id(order_id=order_id)
        items = single_order.json()["data"]["request"]["places"][0]["items"]
        Checking.check_status_code(response=single_order, expected_status_code=200)
        if delivery_service == "Cdek":
            patch_single_order = app.order.patch_order_items_cdek(order_id=order_id, name_1="Бамбук", name_2="Книга")
            Checking.check_status_code(response=patch_single_order, expected_status_code=200)
            Checking.check_json_schema(response=patch_single_order, schema=SCHEMAS.order.order_get_by_id_or_editing)
        elif delivery_service == "FivePost":
            patch_single_order = app.order.patch_order_items_five_post(order_id=order_id, items_name="семена бамбука")
            Checking.check_status_code(response=patch_single_order, expected_status_code=200)
            Checking.check_json_schema(response=patch_single_order, schema=SCHEMAS.order.order_get_by_id_or_editing)
        elif delivery_service == "TopDelivery":
            patch_single_order = app.order.patch_create_multy_order(order_id=order_id, items=items)
            Checking.check_status_code(response=patch_single_order, expected_status_code=200)
            Checking.check_json_schema(response=patch_single_order, schema=SCHEMAS.order.order_get_by_id_or_editing)
        connections.wait_create_order(order_id=order_id)
        order_by_id = app.order.get_order_id(order_id=order_id)
        Checking.check_status_code(response=order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=order_by_id, key_name="status", expected_value="created")
        Checking.checking_json_value(response=order_by_id, key_name="state", expected_value="succeeded")
        assert_order_patch = app.order.get_order_patches(order_id=patch_single_order.json()["id"])
        Checking.check_status_code(response=assert_order_patch, expected_status_code=200)
        Checking.check_json_schema(response=assert_order_patch, schema=SCHEMAS.order.order_get_patches)
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
        check_shared_data(shared_data)
        order_id = choice(shared_data)
        try:
            multi_order = app.order.get_order_id(order_id=order_id)
            Checking.check_status_code(response=multi_order, expected_status_code=200)
            patch_multi_order = app.order.patch_order(order_id=order_id, name="Пуфик", price=500, count=2, weight=2,
                                                      barcode=f"{randrange(1000000, 9999999)}")
            Checking.check_status_code(response=patch_multi_order, expected_status_code=200)
            Checking.check_json_schema(response=patch_multi_order, schema=SCHEMAS.order.order_get_by_id_or_editing)
            connections.wait_create_order(order_id=order_id)
            Checking.checking_json_value(response=patch_multi_order, key_name="status", expected_value="created")
            Checking.checking_json_value(response=patch_multi_order, key_name="state", expected_value="succeeded")
            assert len(multi_order.json()["data"]["request"]["places"]) > \
                   len(patch_multi_order.json()["data"]["request"]["places"])
        except AssertionError:
            if order_id in shared_data:
                shared_data.remove(order_id)
            raise

    @staticmethod
    def test_patch_multi_order_common(app, connections, shared_data, delivery_service=None):
        """Добавление items в многоместный заказ"""
        check_shared_data(shared_data)
        order_id = choice(shared_data)
        try:
            old_len_order_list, patch_order = app.order.patch_order_add_item(order_id=order_id)
            Checking.check_status_code(response=patch_order, expected_status_code=200)
            Checking.check_json_schema(response=patch_order, schema=SCHEMAS.order.order_get_by_id_or_editing)
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
            Checking.checking_json_value(response=new_len_order_list, key_name="state", expected_value="succeeded")
            Checking.checking_sum_len_lists(responses={"PATCH v2/order/{id}": patch_order,
                                                       "GET v2/order/{id} created": old_len_order_list,
                                                       "GET v2/order/{id} patched": new_len_order_list},
                                            old_list=old_len_order_list.json()["data"]["request"]["places"],
                                            new_list=new_len_order_list.json()["data"]["request"]["places"])
        except AssertionError:
            if order_id in shared_data:
                shared_data.remove(order_id)
            raise

    @staticmethod
    def test_editing_order_place_common(app, connections, shared_data):
        """Редактирование грузомест"""
        check_shared_data(shared_data)
        order_id = shared_data.pop()
        patch_order = app.order.patch_order(order_id=order_id, name="Пуфик", price=500, count=2, weight=2)
        Checking.check_status_code(response=patch_order, expected_status_code=200)
        Checking.check_json_schema(response=patch_order, schema=SCHEMAS.order.order_get_by_id_or_editing)
        connections.wait_create_order(order_id=order_id)
        order_by_id = app.order.get_order_id(order_id=order_id)
        Checking.check_status_code(response=order_by_id, expected_status_code=200)
        Checking.checking_json_value(response=order_by_id, key_name="status", expected_value="created")
        Checking.checking_json_value(response=order_by_id, key_name="state", expected_value="succeeded")
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
        check_shared_data(shared_data)
        order_id = choice(shared_data)
        try:
            order_patch = app.order.patch_order_recipient(order_id=order_id, phone_number="+79266967503",
                                                          email="new_test_email@bk.ru", **kwargs)
            Checking.check_status_code(response=order_patch, expected_status_code=200)
            Checking.check_json_schema(response=order_patch, schema=SCHEMAS.order.order_get_by_id_or_editing)
            connections.wait_create_order(order_id=order_patch.json()["id"])
            assert_order_patch = app.order.get_order_patches(order_id=order_patch.json()["id"])
            Checking.check_status_code(response=assert_order_patch, expected_status_code=200)
            Checking.checking_in_list_json_value(response=assert_order_patch, key_name="state",
                                                 expected_value="succeeded")
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
        except AssertionError:
            if order_id in shared_data:
                shared_data.remove(order_id)
            raise

    @staticmethod
    def test_patch_order_weight_common(app, connections, shared_data, delivery_service=None):
        """Редактирование веса в заказе"""
        check_shared_data(shared_data)
        order_id = choice(shared_data)
        try:
            order_patch = app.order.patch_order_weight(order_id=order_id, weight=4)
            Checking.check_status_code(response=order_patch, expected_status_code=200)
            Checking.check_json_schema(response=order_patch, schema=SCHEMAS.order.order_get_by_id_or_editing)
            if delivery_service == "Cdek":
                connections.wait_create_order(order_id=order_id)
                get_order_by_id = app.order.get_order_id(order_id=order_patch.json()["id"])
                Checking.checking_big_json(response=get_order_by_id, key_name="weight", expected_value=4)
            if delivery_service is None:
                Checking.checking_big_json(response=order_patch, key_name="weight", expected_value=4)
        except AssertionError:
            if order_id in shared_data:
                shared_data.remove(order_id)
            raise

    @staticmethod
    def test_get_orders_common(app, shared_data, shared_delivery_service):
        """Получение списка заказов"""
        check_shared_data(shared_data[shared_delivery_service], key="order_ids")
        list_orders = app.order.get_orders()
        Checking.check_status_code(response=list_orders, expected_status_code=200)
        Checking.check_json_schema(response=list_orders, schema=SCHEMAS.order.orders_get)
        Checking.check_response_is_not_empty(response=list_orders)

    @staticmethod
    def test_get_order_by_id_common(app, shared_data):
        """Получение информации о заказе"""
        check_shared_data(shared_data)
        order_id = app.order.get_order_id(order_id=choice(shared_data))
        Checking.check_status_code(response=order_id, expected_status_code=200)
        Checking.check_json_schema(response=order_id, schema=SCHEMAS.order.order_get_by_id_or_editing)

    @staticmethod
    def test_order_details_common(app, shared_data):
        """Получение подробной информации о заказе"""
        check_shared_data(shared_data)
        order_id = choice(shared_data)
        order_details = app.order.get_order_details(order_id=order_id)
        Checking.check_status_code(response=order_details, expected_status_code=200)
        Checking.check_json_schema(response=order_details, schema=SCHEMAS.order.order_get_details)

    @staticmethod
    def test_order_status_common(app, shared_data):
        """Получение информации об истории изменения статусов заказа"""
        check_shared_data(shared_data)
        order_id = choice(shared_data)
        order_status = app.order.get_order_statuses(order_id=order_id)
        Checking.check_status_code(response=order_status, expected_status_code=200)
        Checking.check_json_schema(response=order_status, schema=SCHEMAS.order.order_get_statuses)

    @staticmethod
    def test_get_labels_out_of_parcel_common(app, shared_data, labels=None, format_=None):
        """Получения этикеток вне партии"""
        check_shared_data(shared_data)
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
        check_shared_data(shared_data)
        order_id = choice(shared_data)
        security_code = app.order.get_generate_security_code(order_id=order_id)
        Checking.check_status_code(response=security_code, expected_status_code=200)
        Checking.check_json_schema(response=security_code, schema=SCHEMAS.order.order_generate_security_code)

    @staticmethod
    def test_patch_order_cancelled_common(app, connections, shared_data, delivery_service=None):
        """Отмена заказа"""
        check_shared_data(shared_data)
        order_id = shared_data.pop()
        try:
            custom_headers = {"x-trace-id": "cancelled"} if delivery_service == "Cdek" else None
            order_patch = app.order.patch_order_cancelled(order_id=order_id, headers=custom_headers)
            Checking.check_status_code(response=order_patch, expected_status_code=200)
            Checking.check_json_schema(response=order_patch, schema=SCHEMAS.order.order_get_by_id_or_editing)
            if delivery_service == "Cdek":
                connections.wait_cancelled_order(order_id=order_id)
                get_order_by_id = app.order.get_order_id(order_id=order_patch.json()["id"])
                Checking.checking_json_value(response=get_order_by_id, key_name="state", expected_value="cancelled")
            if delivery_service is None:
                Checking.checking_json_value(response=order_patch, key_name="state", expected_value="cancelled")
        except AssertionError:
            if order_id in shared_data:
                shared_data.remove(order_id)
            raise

    @staticmethod
    def test_delete_order_common(app, connections, shared_data, shared_delivery_service, delivery_service=None):
        """Удаление заказа"""
        check_shared_data(shared_data[shared_delivery_service], key="order_ids")
        order_id = shared_data[shared_delivery_service]["order_ids"].pop()
        delete_order = app.order.delete_order(order_id=order_id)
        Checking.check_status_code(response=delete_order, expected_status_code=204)
        Checking.check_value_comparison(responses={"DELETE v2/order/{id}": delete_order},
                                        one_value=connections.get_list_order_value(order_id=order_id,
                                                                                   value="deleted"),
                                        two_value=[True])
        if delivery_service == "RussianPost":
            lists_to_check = ["orders_courier", "orders_delivery_point", "orders_post_office", "orders_terminal"]
            for list_name in lists_to_check:
                if order_id in shared_data[shared_delivery_service][list_name]:
                    shared_data[shared_delivery_service][list_name].remove(order_id)

    @staticmethod
    def test_create_intake_common(app, shop_id, warehouse_id, delivery_service,  connections,
                                  shared_delivery_service=None, shared_data=None, date=None, intake_external_id=None,
                                  parcel_id=None):
        """Создание забора"""
        new_intake = app.intakes.post_intakes(shop_id=shop_id, warehouse_id=warehouse_id,
                                              delivery_service=delivery_service, date=date,
                                              intake_external_id=intake_external_id, parcel_id=parcel_id)
        Checking.check_status_code(response=new_intake, expected_status_code=201)
        Checking.check_json_schema(response=new_intake, schema=SCHEMAS.intake.intake_create)
        intake_id = new_intake.json()["id"]
        status = connections.get_list_intakes_value(intake_id=intake_id, value="status")
        if delivery_service == "Cdek":
            expected_status = ["pending"]
        else:
            expected_status = ["created"]
        Checking.check_value_comparison(responses={"POST v2/intakes": new_intake},
                                        one_value=status, two_value=expected_status)
        if shared_data is not None:
            shared_data[shared_delivery_service]["intake_id"] = intake_id

    @staticmethod
    def test_patch_intake_common(app, connections, expected_status, **kwargs):
        """Редактирование забора"""
        patch_intake = app.intakes.patch_intakes(**kwargs)
        Checking.check_status_code(response=patch_intake, expected_status_code=200)
        Checking.check_json_schema(response=patch_intake, schema=SCHEMAS.intake.intake_get_by_id_or_patch)
        status = connections.get_list_intakes_value(intake_id=patch_intake.json()["id"], value="status")
        Checking.check_value_comparison(responses={"POST v2/intakes": patch_intake},
                                        one_value=status, two_value=expected_status)

    @staticmethod
    def test_intake_time_schedules_common(app, shared_data, shop_id, warehouse_id, delivery_service_code):
        intake_time_schedules = app.intakes.intake_time_schedules(shop_id=shop_id, warehouse_id=warehouse_id,
                                                                  delivery_service_code=delivery_service_code)
        Checking.check_status_code(response=intake_time_schedules, expected_status_code=200)
        Checking.check_json_schema(response=intake_time_schedules, schema=SCHEMAS.intake.intake_time_schedules)

        data = intake_time_schedules.json()
        intervals = data.get("intervals", [])
        if not intervals:
            raise AssertionError("Не найдено ни одного интервала для забора")
        first_interval = intervals[0]
        shared_data["intake_date"] = first_interval["date"]
        shared_data["intake_external_id"] = first_interval["externalTimeIntervalId"]
