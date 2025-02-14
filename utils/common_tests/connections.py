import allure
from utils.global_enums import INFO
from utils.checking import Checking
from utils.response_schemas import SCHEMAS


class CommonConnections:

    @staticmethod
    def connecting_delivery_services_common(app, shop_id, connection_settings, code=None, aggregation: bool = None):
        try:
            response = app.service.post_delivery_service(shop_id=shop_id,
                                                         delivery_service=connection_settings)
            Checking.check_status_code(response=response, expected_status_code=201)
            Checking.check_json_schema(response=response, schema=SCHEMAS.connections.connection_create)
            if code:
                get_connection = app.service.get_delivery_services_code(shop_id=shop_id, code=code)
                Checking.check_json_schema(response=get_connection,
                                           schema=SCHEMAS.connections.connection_get_by_id_or_editing)
                Checking.check_response_key_values(response=get_connection, key_values={
                    ("credentials", "active"): True,
                    ("credentials", "visibility"): True,
                    ("credentials", "data", "externalDeliveryCode"): None,
                    ("credentials", "data", "metashipInform"): None
                })
                if aggregation:
                    Checking.check_response_key_values(response=get_connection, key_values={
                        ("credentials", "data", "type"): "aggregation",
                        ("credentials", "data", "moderation"): True,
                        ("hasAggregation",): True
                    })
                else:
                    Checking.checking_json_key_value(response=get_connection, key_path=["credentials", "data", "type"],
                                                     expected_value="integration")
        except Exception as e:
            allure.attach(f"Ошибка при подключении настроек СД: {str(e)}", attachment_type=allure.attachment_type.TEXT)
            raise e

    @staticmethod
    def update_connection_id_common(admin, shop_id, delivery_service, update_settings):
        try:
            response = admin.connection.put_update_connection_id(shop_id=shop_id, delivery_service=delivery_service,
                                                                 settings=update_settings)
            Checking.check_status_code(response=response, expected_status_code=200)
            Checking.checking_json_key(response=response, expected_value=INFO.entity_connections_id)
        except Exception as e:
            allure.attach(f"Ошибка при обновлении идентификатора подключения: {str(e)}",
                          attachment_type=allure.attachment_type.TEXT)
            raise e

    @staticmethod
    def moderation_delivery_services_common(admin, shop_id, moderation_settings):
        try:
            response = admin.connection.post_connections(delivery_service=moderation_settings(shop_id))
            Checking.check_status_code(response=response, expected_status_code=200)
            Checking.checking_json_key(response=response, expected_value=INFO.entity_moderation)
        except Exception as e:
            allure.attach(f"Ошибка при модерации СД: {str(e)}", attachment_type=allure.attachment_type.TEXT)
            raise e

    @staticmethod
    def connect_aggregation_services_common(app, admin, shop_id, connection_settings, moderation_settings,
                                            code=None, delivery_service=None, update_settings=None):
        CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                              connection_settings=connection_settings, code=code,
                                                              aggregation=True)
        if update_settings:
            CommonConnections.update_connection_id_common(admin, shop_id, delivery_service,
                                                          update_settings=update_settings)
        CommonConnections.moderation_delivery_services_common(admin=admin, shop_id=shop_id,
                                                              moderation_settings=moderation_settings)
        if code:
            get_connection = app.service.get_delivery_services_code(shop_id=shop_id, code=code)
            Checking.checking_json_key_value(response=get_connection, key_path=["credentials", "data", "moderation"],
                                             expected_value=False)

    @staticmethod
    def test_get_delivery_services_common(app, shop_id):
        response = app.service.get_delivery_services(shop_id=shop_id)
        Checking.check_status_code(response=response, expected_status_code=200)
        Checking.check_json_schema(response=response, schema=SCHEMAS.connections.connection_get)

    @staticmethod
    def test_patch_delivery_service_common(app, shop_id, code):
        response = app.service.patch_delivery_service(shop_id=shop_id, code=code, tariffs=["14", "25"],
                                                      visibility=False)
        Checking.check_status_code(response=response, expected_status_code=200)
        Checking.check_json_schema(response=response,
                                   schema=SCHEMAS.connections.connection_get_by_id_or_editing)
        Checking.check_response_key_values(response=response, key_values={
            ("credentials", "active"): True,
            ("credentials", "visibility"): False,
            ("credentials", "settings", "tariffs", "restrict"): None,
            ("credentials", "settings", "tariffs", "exclude"): ["14", "25"]
        })

    @staticmethod
    def test_put_delivery_service_common(app, shop_id, code, connection_settings, data, types=None):
        response = app.service.put_delivery_service(shop_id=shop_id, code=code, connection_settings=connection_settings)
        if types == "aggregation":
            Checking.check_status_code(response=response, expected_status_code=409)
        else:
            Checking.check_status_code(response=response, expected_status_code=204)
            get_connection_response = app.service.get_delivery_services_code(shop_id=shop_id, code=code)
            Checking.check_json_schema(response=get_connection_response,
                                       schema=SCHEMAS.connections.connection_get_by_id_or_editing)
            for key, expected_value in data.items():
                Checking.checking_json_key_value(response=get_connection_response,
                                                 key_path=["credentials", "data", key], expected_value=expected_value)

    @staticmethod
    def test_deactivate_delivery_service_common(app, shop_id, code):
        response = app.service.post_deactivate_delivery_service(shop_id=shop_id, code=code)
        Checking.check_status_code(response=response, expected_status_code=204)
        get_connection_response = app.service.get_delivery_services_code(shop_id=shop_id, code=code)
        Checking.check_json_schema(response=get_connection_response,
                                   schema=SCHEMAS.connections.connection_get_by_id_or_editing)
        Checking.checking_json_key_value(response=get_connection_response, key_path=["credentials", "active"],
                                         expected_value=False)

    @staticmethod
    def test_activate_delivery_service_common(app, shop_id, code):
        response = app.service.post_activate_delivery_service(shop_id=shop_id, code=code)
        Checking.check_status_code(response=response, expected_status_code=204)
        get_connection_response = app.service.get_delivery_services_code(shop_id=shop_id, code=code)
        Checking.check_json_schema(response=get_connection_response,
                                   schema=SCHEMAS.connections.connection_get_by_id_or_editing)
        Checking.checking_json_key_value(response=get_connection_response, key_path=["credentials", "active"],
                                         expected_value=True)
