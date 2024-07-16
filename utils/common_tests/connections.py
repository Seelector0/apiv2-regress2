import allure
from utils.global_enums import INFO
from utils.checking import Checking


class CommonConnections:

    @staticmethod
    def connecting_delivery_services_common(app, shop_id, connection_settings):
        try:
            response = app.service.post_delivery_service(shop_id=shop_id,
                                                         delivery_service=connection_settings)
            Checking.check_status_code(response=response, expected_status_code=201)
            Checking.checking_json_key(response=response, expected_value=INFO.created_entity)
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
    def connect_aggregation_services_common(app, admin, shop_id, connection_settings,
                                            moderation_settings, delivery_service=None, update_settings=None):
        CommonConnections.connecting_delivery_services_common(app=app, shop_id=shop_id,
                                                              connection_settings=connection_settings)
        if update_settings:
            CommonConnections.update_connection_id_common(admin, shop_id, delivery_service,
                                                          update_settings=update_settings)
        CommonConnections.moderation_delivery_services_common(admin=admin, shop_id=shop_id,
                                                              moderation_settings=moderation_settings)
