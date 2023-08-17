from utils.dicts import DICT_OBJECT
import requests.exceptions
import simplejson.errors
import allure


class ApiShop:

    def __init__(self, app):
        self.app = app
        self.link = "customer/shops"

    def post_shop(self):
        """Метод создания магазина."""
        shop = DICT_OBJECT.form_shop_body()
        result = self.app.http_method.post(link=self.link, data=shop)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_shops(self):
        """Метод получения списка магазинов."""
        result = self.app.http_method.get(link=self.link)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def get_shop_id(self, shop_id: str):
        """Метод получения магазина по его id.
        :param shop_id: Идентификатор магазина.
        """
        result = self.app.http_method.get(link=f"{self.link}/{shop_id}")
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def put_shop(self, shop_id: str, shop_name: str, shop_url: str, contact_person: str, phone: str):
        r"""Метод обновления магазина.
        :param shop_id: Идентификатор магазина.
        :param shop_name: Название магазина
        :param shop_url: URL адрес магазина
        :param contact_person: ФИО контактного лица магазина.
        :param phone: Телефон контактного лица магазина.
        """
        put_shop = DICT_OBJECT.form_shop_body()
        put_shop["name"] = shop_name
        put_shop["uri"] = shop_url
        put_shop["phone"] = phone
        put_shop["sender"] = contact_person
        return self.app.http_method.put(link=f"{self.link}/{shop_id}", data=put_shop)

    def patch_shop(self, shop_id: str, value: bool = True):
        r"""Метод обновления полей магазина.
        :param shop_id: Идентификатор магазина.
        :param value: Флаг скрывает магазин из ЛК.
        """
        patch_shop = DICT_OBJECT.form_patch_body(op="replace", path="visibility", value=value)
        result = self.app.http_method.patch(link=f"{self.link}/{shop_id}", data=patch_shop)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")
