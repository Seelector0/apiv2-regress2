class ApiDeliveryServices:

    def __init__(self, app):
        self.app = app

    def link_delivery_services(self, shop_id):
        r"""Метод получения ссылки для подключения СД."""
        return f"{self.app.shop.link}/{shop_id}/delivery_services"

    def post_delivery_service(self, delivery_service: dict, shop_id):
        result = self.app.http_method.post(link=self.link_delivery_services(shop_id=shop_id), json=delivery_service)
        return self.app.http_method.return_result(response=result)

    def get_delivery_services(self, shop_id):
        """Метод получения списка выполненных настроек СД к магазину."""
        result = self.app.http_method.get(link=self.link_delivery_services(shop_id=shop_id))
        return self.app.http_method.return_result(response=result)

    def get_delivery_services_code(self, shop_id, code: str):
        r"""Получение настроек подключения к СД по id магазина.
        :param shop_id: Id магазина.
        :param code: Код СД.
        """
        result = self.app.http_method.get(link=f"{self.link_delivery_services(shop_id=shop_id)}/{code}")
        return self.app.http_method.return_result(response=result)

    def patch_delivery_service(self, shop_id, code: str, tariffs: list, visibility: bool):
        """
        Метод для обновления тарифов и настроек видимости службы доставки.

        :param shop_id: Id магазина.
        :param code: Код службы доставки.
        :param tariffs: Тарифы службы доставки (если указано, будут обновлены тарифы).
        :param visibility: Видимость службы доставки (если указано, будет обновлена видимость).
        """
        tariffs_patch = self.app.dicts.form_patch_body(
            op="replace",
            path="settings.tariffs",
            value=self.app.dicts.settings_tariffs(tariffs=tariffs)
        )
        visibility_patch = self.app.dicts.form_patch_body(
            op="replace",
            path="visibility",
            value=visibility
        )
        result = self.app.http_method.patch(
            link=f"{self.link_delivery_services(shop_id=shop_id)}/{code}",
            json=[*visibility_patch, *tariffs_patch]
        )
        return self.app.http_method.return_result(response=result)

    def put_delivery_service(self, shop_id, code: str, connection_settings: dict):
        r"""Активация настроек подключения к СД по id магазина.
        :param shop_id: Id магазина.
        :param code: Код СД.
        :param connection_settings: данные подключения СД.
        """
        result = self.app.http_method.put(f"{self.link_delivery_services(shop_id=shop_id)}/{code}",
                                          json=connection_settings)
        return self.app.http_method.return_result(response=result)

    def post_activate_delivery_service(self, shop_id, code: str):
        r"""Активация настроек подключения к СД по id магазина.
        :param shop_id: Id магазина.
        :param code: Код СД.
        """
        return self.app.http_method.post(link=f"{self.link_delivery_services(shop_id=shop_id)}/{code}/activate")

    def post_deactivate_delivery_service(self, shop_id, code: str):
        r"""Деактивация настроек подключения к СД по id магазина.
        :param shop_id: Id магазина.
        :param code: Код СД.
        """
        return self.app.http_method.post(link=f"{self.link_delivery_services(shop_id=shop_id)}/{code}/deactivate")
