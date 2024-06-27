from databases.customer_api import DataBaseCustomerApi
from databases.connections import DataBaseConnections


class ApiConnectionDeliveryServices:

    def __init__(self, admin):
        self.admin = admin
        self.link = "configurations"
        self.db_connections = DataBaseConnections()
        self.db_customer_api = DataBaseCustomerApi()

    def post_connections(self, delivery_service: dict):
        """Снятие с модерации СД Cdek."""
        result = self.admin.http_method.post(link=self.link, json=delivery_service, admin=True)
        return self.admin.http_method.return_result(response=result)

    def put_update_connection_id(self, shop_id, delivery_service, settings: dict):
        r"""Обновления подключения СД.
        :param settings: Настройки для разных СД.
        :param shop_id: Id магазина.
        :param delivery_service: Название сд.
        """
        connections_id = self.db_customer_api.get_connections_id(shop_id=shop_id, delivery_service=delivery_service)
        put_update = self.admin.dicts.form_update_connection(settings=settings)
        result = self.admin.http_method.put(link=f"connection/{connections_id}", json=put_update, admin=True)
        return self.admin.http_method.return_result(response=result)
