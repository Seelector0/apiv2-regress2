from dotenv import load_dotenv, find_dotenv
from utils.dicts import DICT_OBJECT
import requests.exceptions
import simplejson.errors
import allure
import os


class ApiModerationDeliveryServices:

    load_dotenv(find_dotenv())

    def __init__(self, admin):
        self.admin = admin
        self.link = "configurations"

    def moderation_russian_post(self):
        """Снятие с модерация СД RussianPost."""
        russian_post = DICT_OBJECT.form_moderation_delivery_services(delivery_service_code="RussianPost")
        russian_post["credential"]["token"] = f"{os.getenv('RP_TOKEN')}"
        russian_post["credential"]["secret"] = f"{os.getenv('RP_SECRET')}"
        result = self.admin.http_method.post(link=self.link, json=russian_post, admin=True)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def moderation_topdelivery(self):
        """Снятие с модерации СД TopDelivery."""
        topdelivery = DICT_OBJECT.form_moderation_delivery_services(delivery_service_code="TopDelivery")
        topdelivery["credential"]["username"] = f"{os.getenv('TD_USER_NAME')}"
        topdelivery["credential"]["password"] = f"{os.getenv('TD_PASSWORD')}"
        topdelivery["credential"]["basicLogin"] = f"{os.getenv('TD_BASIC_LOGIN')}"
        topdelivery["credential"]["basicPassword"] = f"{os.getenv('TD_BASIC_PASSWORD')}"
        result = self.admin.http_method.post(link=self.link, json=topdelivery, admin=True)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def moderation_boxberry(self):
        """Снятие с модерации СД Boxberry."""
        boxberry = DICT_OBJECT.form_moderation_delivery_services(delivery_service_code="Boxberry")
        boxberry["credential"]["token"] = f"{os.getenv('BB_API_TOKEN')}"
        result = self.admin.http_method.post(link=self.link, json=boxberry, admin=True)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def moderation_cdek(self):
        """Снятие с модерации СД Cdek."""
        cdek = DICT_OBJECT.form_moderation_delivery_services(delivery_service_code="Cdek")
        cdek["credential"]["account"] = f"{os.getenv('CDEK_ACCOUNT')}"
        cdek["credential"]["password"] = f"{os.getenv('CDEK_PASSWORD')}"
        result = self.admin.http_method.post(link=self.link, json=cdek, admin=True)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def moderation_dpd(self):
        """Снятие с модерации СД Dpd."""
        dpd = DICT_OBJECT.form_moderation_delivery_services(delivery_service_code="Dpd")
        dpd["credential"]["clientNumber"] = f"{os.getenv('DPD_CLIENT_NUMBER')}"
        dpd["credential"]["clientKey"] = f"{os.getenv('DPD_CLIENT_KEY')}"
        result = self.admin.http_method.post(link=self.link, json=dpd, admin=True)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def moderation_five_post(self):
        """Снятие с модерации СД FivePost"""
        five_post = DICT_OBJECT.form_moderation_delivery_services(delivery_service_code="FivePost")
        five_post["credential"]["apiKey"] = f"{os.getenv('FIVE_POST_API_KEY')}"
        five_post["credential"]["partnerNumber"] = f"{os.getenv('FIVE_POST_PARTNER_NUMBER')}"
        five_post["credential"]["baseWeight"] = int(f"{os.getenv('FIVE_POST_BASE_WEIGHT')}")
        result = self.admin.http_method.post(link=self.link, json=five_post, admin=True)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def moderation_yandex_go(self):
        """Снятие с модерации СД YandexGo"""
        yandex_go = DICT_OBJECT.form_moderation_delivery_services(delivery_service_code="YandexGo")
        yandex_go["credential"]["yandexGoToken"] = f"{os.getenv('YA_GO_TOKEN')}"
        yandex_go["credential"]["inn"] = "7734381257"
        result = self.admin.http_method.post(link=self.link, json=yandex_go, admin=True)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def moderation_yandex_delivery(self):
        """Снятие с модерации СД YandexDelivery"""
        yandex_delivery = DICT_OBJECT.form_moderation_delivery_services(delivery_service_code="YandexDelivery")
        yandex_delivery["credential"]["yandexDeliveryToken"] = f"{os.getenv('YA_DELIVERY_TOKEN')}"
        yandex_delivery["credential"]["inn"] = f"{os.getenv('YA_DELIVERY_INN')}"
        yandex_delivery["credential"]["intakePointCode"] = f"{os.getenv('YA_DELIVERY_INTAKE_POINT_CODE')}"
        result = self.admin.http_method.post(link=self.link, json=yandex_delivery, admin=True)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")

    def moderation_dalli(self):
        """Снятие с модерации СД Dalli"""
        dalli = DICT_OBJECT.form_moderation_delivery_services(delivery_service_code="Dalli")
        dalli["credential"]["token"] = f"{os.getenv('DALLI_TOKEN')}"
        result = self.admin.http_method.post(link=self.link, json=dalli, admin=True)
        try:
            with allure.step(title=f"Response: {result.json()}"):
                return result
        except simplejson.errors.JSONDecodeError or requests.exceptions.JSONDecodeError:
            raise AssertionError(f"API method Failed\nResponse status code: {result.status_code}")
