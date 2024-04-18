from databases.connections import DataBaseConnections


class ApiDeliveryServices:

    def __init__(self, app):
        self.app = app
        self.db_connections = DataBaseConnections()

    def link_delivery_services(self, index_shop_id: int = 0):
        r"""Метод получения ссылки для подключения СД.
        :param index_shop_id: Индекс магазина.
        """
        return f"{self.app.shop.link}/{self.db_connections.get_list_shops()[index_shop_id]}/delivery_services"

    def post_delivery_service(self, delivery_service: dict):
        result = self.app.http_method.post(link=self.link_delivery_services(), json=delivery_service)
        return self.app.http_method.return_result(response=result)

    def get_delivery_services(self):
        """Метод получения списка выполненных настроек СД к магазину."""
        result = self.app.http_method.get(link=self.link_delivery_services())
        return self.app.http_method.return_result(response=result)

    def get_delivery_services_code(self, code: str):
        r"""Получение настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        result = self.app.http_method.get(link=f"{self.link_delivery_services()}/{code}")
        return self.app.http_method.return_result(response=result)

    def patch_delivery_services_tariffs(self, code: str, tariffs):
        r"""Метод редактирования тарифов СД.
        :param code: Код СД.
        :param tariffs: Тарифы СД.
        """
        patch = self.app.dicts.form_patch_body(op="replace", path="settings.tariffs",
                                               value=self.app.dicts.settings_tariffs(tariffs=tariffs))
        result = self.app.http_method.patch(link=f"{self.link_delivery_services()}/{code}", json=patch)
        return self.app.http_method.return_result(response=result)

    def patch_delivery_services(self, code: str, value: bool = True):
        r"""Метод редактирования полей настройки подключения к СД.
        :param code: Код СД.
        :param value: Скрытие СД из ЛК при False.
        """
        patch = self.app.dicts.form_patch_body(op="replace", path="visibility", value=value)
        result = self.app.http_method.patch(link=f"{self.link_delivery_services()}/{code}", json=patch)
        return self.app.http_method.return_result(response=result)

    def post_activate_delivery_service(self, code: str):
        r"""Активация настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        return self.app.http_method.post(link=f"{self.link_delivery_services()}/{code}/activate")

    def post_deactivate_delivery_service(self, code: str):
        r"""Деактивация настроек подключения к СД по id магазина.
        :param code: Код СД.
        """
        return self.app.http_method.post(link=f"{self.link_delivery_services()}/{code}/deactivate")
