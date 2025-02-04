from random import choice
from utils.checking import Checking
from utils.global_enums import INFO
from utils.response_schemas import SCHEMAS
from utils.utils import check_shared_data


class CommonParcels:

    @staticmethod
    def create_parcel_common(app, shared_data, shared_delivery_service, types=None, **kwargs):
        """Создание партии"""
        if types:
            check_shared_data(shared_data[shared_delivery_service], key=types)
            order = shared_data[shared_delivery_service][types].pop()
        else:
            check_shared_data(shared_data[shared_delivery_service], key="order_ids")
            order = shared_data[shared_delivery_service]["order_ids"].pop()
        create_parcel = app.parcel.post_parcel(value=order, **kwargs)
        Checking.check_status_code(response=create_parcel, expected_status_code=207)
        Checking.check_json_schema(response=create_parcel, schema=SCHEMAS.parcel.parcels_create)
        parcel_id = create_parcel.json()[0]["id"]
        shared_data[shared_delivery_service]["parcel_ids"].append(parcel_id)
        shared_data[shared_delivery_service]["order_ids_in_parcel"].append(order)
        if types == "orders_courier":
            shared_data[shared_delivery_service]["parcel_ids_courier"].append(parcel_id)
        elif types == "orders_post_office":
            shared_data[shared_delivery_service]["parcel_ids_post_office"].append(parcel_id)
        elif types == "orders_delivery_point":
            shared_data[shared_delivery_service]["parcel_ids_delivery_point"].append(parcel_id)
        elif types == "orders_terminal":
            shared_data[shared_delivery_service]["parcel_ids_terminal"].append(parcel_id)

    @staticmethod
    def test_patch_weight_random_order_in_parcel_common(app, connections, shared_data):
        """Редактирование веса заказа в партии"""
        check_shared_data(shared_data)
        order_id = choice(shared_data)
        try:
            order_patch = app.order.patch_order_weight(order_id=order_id, weight=4)
            Checking.check_status_code(response=order_patch, expected_status_code=200)
            connections.wait_create_order(order_id=order_patch.json()["id"])
            get_order_by_id = app.order.get_order_id(order_id=order_patch.json()["id"])
            Checking.checking_big_json(response=get_order_by_id, key_name="weight", expected_value=4)
        except AssertionError:
            if order_id in shared_data:
                shared_data.remove(order_id)
            raise

    @staticmethod
    def test_get_parcels_common(app, shared_delivery_service, shared_data):
        """Получение списка партий CД RussianPost"""
        check_shared_data(shared_data[shared_delivery_service], key="order_ids_in_parcel")
        list_parcel = app.parcel.get_parcels()
        Checking.check_status_code(response=list_parcel, expected_status_code=200)
        Checking.check_response_is_not_empty(response=list_parcel)
        Checking.check_json_schema(response=list_parcel, schema=SCHEMAS.parcel.parcels_get)

    @staticmethod
    def test_get_parcel_by_id_common(app, shared_data):
        """Получение информации о партии СД RussianPost"""
        check_shared_data(shared_data)
        parcel_id = app.parcel.get_parcel_id(parcel_id=choice(shared_data))
        Checking.check_status_code(response=parcel_id, expected_status_code=200)
        Checking.checking_json_key(response=parcel_id, expected_value=INFO.entity_parcel)

    @staticmethod
    def add_order_in_parcel_common(app, connections, shared_data, shared_delivery_service, types=None):
        """Добавление заказов в партию"""
        if types:
            check_shared_data(shared_data[shared_delivery_service], key=types)
            orders = shared_data[shared_delivery_service][types]
        else:
            check_shared_data(shared_data[shared_delivery_service], key="order_ids")
            orders = shared_data[shared_delivery_service]["order_ids"]

        order = choice(orders)

        if types == "orders_courier":
            parcel_id = choice(shared_data[shared_delivery_service]["parcel_ids_courier"])
        elif types == "orders_post_office":
            parcel_id = choice(shared_data[shared_delivery_service]["parcel_ids_post_office"])
        elif types == "orders_delivery_point":
            parcel_id = choice(shared_data[shared_delivery_service]["parcel_ids_delivery_point"])
        elif types == "orders_terminal":
            parcel_id = choice(shared_data[shared_delivery_service]["parcel_ids_terminal"])
        else:
            parcel_id = choice(shared_data[shared_delivery_service]["parcel_ids"])
        parcel_add = app.parcel.patch_parcel(order_id=order, parcel_id=parcel_id, op="add")
        Checking.check_status_code(response=parcel_add, expected_status_code=200)
        shared_data[shared_delivery_service]["order_ids_in_parcel"].append(order)
        assert order in connections.get_list_all_orders_in_parcel_for_parcel_id(parcel_id=parcel_id)

    @staticmethod
    def test_change_shipment_date_common(app, shared_data):
        """Редактирование партии СД (Изменение даты отправки партии)"""
        check_shared_data(shared_data)
        parcel_id = choice(shared_data)
        shipment_date = app.parcel.patch_parcel_shipment_date(parcel_id=parcel_id, day=5)
        Checking.check_status_code(response=shipment_date, expected_status_code=200)
        new_date = shipment_date.json()["data"]["request"]["shipmentDate"]
        Checking.check_date_change(response=shipment_date, calendar_date=new_date, number_of_days=5)

    @staticmethod
    def test_get_label_common(app, shared_data, labels=None, format_=None):
        """Получение этикетки СД"""
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
    def test_get_labels_from_parcel_common(app, shared_delivery_service, shared_data):
        """Получение этикеток заказов из партии"""
        check_shared_data(shared_data[shared_delivery_service], key="parcel_ids")
        labels_from_parcel = app.document.post_labels(
            parcel_id=choice(shared_data[shared_delivery_service]["parcel_ids"]),
            order_ids=shared_data[shared_delivery_service]["order_ids_in_parcel"])
        Checking.check_status_code(response=labels_from_parcel, expected_status_code=200)

    @staticmethod
    def test_get_app_common(app, shared_data):
        """Получение АПП"""
        check_shared_data(shared_data)
        acceptance = app.document.get_acceptance(parcel_id=choice(shared_data))
        Checking.check_status_code(response=acceptance, expected_status_code=200)

    @staticmethod
    def test_get_documents_common(app, shared_data):
        """Получение документов архивом"""
        check_shared_data(shared_data)
        documents = app.document.get_files(parcel_id=choice(shared_data))
        Checking.check_status_code(response=documents, expected_status_code=200)

    @staticmethod
    def test_forms_parcels_labels_common(app, shared_data):
        """Создание формы с этикетками партии"""
        check_shared_data(shared_data)
        forms_labels = app.forms.post_forms(parcel_id=choice(shared_data))
        Checking.check_status_code(response=forms_labels, expected_status_code=201)
        Checking.checking_json_key(response=forms_labels, expected_value=INFO.entity_forms_parcels_labels)

    @staticmethod
    def test_remove_order_in_parcel_common(app, connections, shared_delivery_service, shared_data):
        """Редактирование партии (Удаление заказа из партии)"""
        check_shared_data(shared_data[shared_delivery_service], key="order_ids_in_parcel")
        remove_order = app.parcel.patch_parcel(op="remove",
                                               parcel_id=choice(shared_data[shared_delivery_service]["parcel_ids"]),
                                               order_id=choice
                                               (shared_data[shared_delivery_service]["order_ids_in_parcel"]))
        Checking.check_status_code(response=remove_order, expected_status_code=200)
        assert remove_order is not connections.get_list_all_orders_in_parcel()
