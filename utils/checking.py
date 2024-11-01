from typing import List, Dict, Any

from requests import Response
import datetime
import allure
import json


class Checking:

    @staticmethod
    def _assert_with_trace(response: Response, condition: bool, message: str):
        """Проверяет условие и добавляет x-trace-id в сообщение об ошибке."""
        x_trace_id = response.request.headers.get("x-trace-id", "No x-trace-id")
        assert condition, f"{message} | x-trace-id: {x_trace_id}"

    @staticmethod
    def check_status_code(response: Response, expected_status_code: int):
        """Проверяет статус код ответа."""
        with allure.step(title=f"Проверка что статус код равен {expected_status_code}"):
            Checking._assert_with_trace(response=response, condition=response.status_code == expected_status_code,
                                        message=f"Не ожидаемый статус код! Ожидаемый: {expected_status_code}. "
                                                f"Фактический: {response.status_code}")

    @staticmethod
    def checking_json_key(response: Response, expected_value: list):
        """Проверяет наличие обязательных ключей в JSON-ответе."""
        with allure.step(title=f"Проверка что в ответе есть ключи {expected_value}"):
            Checking._assert_with_trace(response=response, condition=list(json.loads(response.text)) == expected_value,
                                        message=f"Не ожидаемые ключи! Ожидаемые {expected_value}. "
                                                f"Фактические {list(json.loads(response.text))}")

    @staticmethod
    def checking_json_contains(response: Response, expected_values: List[Dict[str, Any]]):
        """Проверяет наличие обязательных элементов в JSON-ответе."""
        with allure.step(f"Проверка, что JSON-ответ содержит все ожидаемые элементы: {expected_values}"):
            response_data = response.json()
            missing_elements = [item for item in expected_values if item not in response_data]
            Checking._assert_with_trace(response=response, condition=len(missing_elements) == 0,
                                        message=f"Не найдены ожидаемые элементы: {missing_elements}. "
                                                f"Фактический ответ: {response_data}")

    @staticmethod
    def checking_json_value(response: Response, key_name: str, expected_value, field=None):
        """Проверяет значение по ключу в JSON-ответе."""
        with allure.step(title=f"Проверка что в ответе есть значение {expected_value}"):
            if field is None:
                Checking._assert_with_trace(response=response, condition=response.json()[key_name] == expected_value,
                                            message=f"Не совпадает значение! Ожидаемое значение {expected_value}!!! "
                                                    f"Фактическое значение {response.json()[key_name]}")
            else:
                Checking._assert_with_trace(response=response,
                                            condition=response.json()[key_name][field] == expected_value,
                                            message=f"Не совпадает значение! У ключа {response.json()[key_name][field]}"
                                                    f" фактическое значение {expected_value}")

    @staticmethod
    def checking_big_json(response: Response, key_name: str, expected_value, field=None):
        """Проверяет значение по ключу в большом JSON-ответе."""
        with allure.step(title=f"Проверка что в ответе есть значение {expected_value}"):
            check = response.json()["data"]["request"]
            if field is None:
                Checking._assert_with_trace(response=response, condition=check.get(key_name) == expected_value,
                                            message=f"Не совпадает значение! Ожидаемое значение {expected_value}!!! "
                                                    f"Фактическое значение {check.get(key_name)}")
            else:
                Checking._assert_with_trace(response=response, condition=check.get(key_name)[field] == expected_value,
                                            message=f"Не совпадает значение! У ключа {check.get(key_name)[field]} "
                                                    f"фактическое значение {expected_value}")

    @staticmethod
    def checking_in_list_json_value(response: Response, key_name, expected_value):
        """Проверяет наличие значения в списке объектов JSON-ответа."""
        with allure.step(title=f"Проверка что в списке есть значение {expected_value}"):
            for element in response.json():
                Checking._assert_with_trace(response=response, condition=element[key_name] == expected_value,
                                            message=f"Не ожидаемое значение! Ожидаемое значение {expected_value}!!! "
                                                    f"Фактическое значение {element[key_name]}")

    @staticmethod
    def check_keys_present_in_list_items(response: Response, key_names, list_key):
        """Проверяет, что в каждом объекте списка под ключом `list_key` есть указанные ключи."""
        with allure.step(
                title=f"Проверка, что в каждом объекте списка '{list_key}' есть значения для ключей {key_names}"):
            items_list = response.json()[list_key]
            for element in items_list:
                for key in key_names:
                    Checking._assert_with_trace(response=response, condition=key in element,
                                                message=f"Значение для ключа '{key}' "
                                                        f"отсутствует или равно None в объекте {element}!")

    @staticmethod
    def checking_sum_len_lists(responses: dict, old_list: list, new_list: list):
        """Проверяет увеличение длины списка при переходе от старого списка к новому."""
        response_info = ', '.join(
            f"{name}: x-trace-id: {resp.request.headers.get('x-trace-id', 'No x-trace-id')}"
            for name, resp in responses.items())
        with allure.step(title="Проверка длины списков"):
            condition = len(old_list) + 1 == len(new_list)
            assert condition, (f"Длина списков одинаковая! Старый список: {len(old_list)}, "
                               f"Новый список: {len(new_list)} | {response_info}")

    @staticmethod
    def check_date_change(response: Response, calendar_date, number_of_days: int):
        """Проверяет изменение даты на заданное количество дней."""
        with allure.step(title=f"Проверка, что дата отправки изменилась на {number_of_days} день/дней"):
            day = datetime.date.today()
            day += datetime.timedelta(days=number_of_days)
            Checking._assert_with_trace(response=response, condition=calendar_date == str(day),
                                        message=f"Дата {calendar_date} не соответствует ожидаемой дате {day}")

    @staticmethod
    def check_value_comparison(responses: dict, one_value, two_value):
        """Сравнивает два значения на равенство."""
        response_info = ', '.join(
            f"{name}: x-trace-id: {resp.request.headers.get('x-trace-id', 'No x-trace-id')}"
            for name, resp in responses.items())
        with allure.step(title="Проверка двух значений на равенство"):
            condition = one_value == two_value
            assert condition, (f"Значения не равны!Первое значение: {one_value}, "
                               f"второе значение: {two_value}| {response_info}")

    @staticmethod
    def check_delivery_services_in_widget_offers(response: Response, delivery_service: str):
        """Проверяет наличие службы доставки в ответе от виджета предложений."""
        with allure.step(title=f"Проверка что в ответе есть СД {delivery_service}"):
            Checking._assert_with_trace(response=response, condition=response.json()["features"] != [],
                                        message=f"Список служб доставки пуст: {response.json()['features']}")
            for i in response.json()["features"]:
                Checking._assert_with_trace(response=response,
                                            condition=i["point"]["deliveryServiceCode"] == delivery_service,
                                            message=f"Служба доставки {delivery_service} не найдена в ответе")

    @staticmethod
    def check_response_is_not_empty(response: Response):
        """Проверяет, что ответ не пустой."""
        with allure.step(title="Проверка, что ответ не пустой"):
            Checking._assert_with_trace(response=response, condition=len(response.json()) != 0,
                                        message=f"Ответ пустой! Ответ: {response.json()}, "
                                                f"длинна ответа {len(response.json())}")
