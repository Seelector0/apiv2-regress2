import datetime
from requests import Response
import allure
import json


class Checking:

    @staticmethod
    def check_status_code(response: Response, expected_status_code: int):
        """Метод для проверки статус кода"""
        with allure.step(f"Проверяю что статус код равен {expected_status_code}"):
            assert response.status_code == expected_status_code, \
                f"Не ожидаемый status code! Ожидаемый: {expected_status_code}. Фактический: {response.status_code}"

    @staticmethod
    def checking_json_key(response: Response, expected_value: list):
        """Метод для проверки обязательных полей (ключей) в ответе"""
        with allure.step(f"Проверяю что в ответе есть ключи {expected_value}"):
            token = json.loads(response.text)
            assert list(token) == expected_value, \
                f"Не ожидаемые ключи! Ожидаемые {expected_value}. Фактические {list(token)}"

    @staticmethod
    def checking_json_value(response: Response, key_name: str, expected_value, field=None):
        """Метод для проверки обязательного ключа в ответе"""
        with allure.step(f"Проверяю что в ответе есть значение {expected_value}"):
            if field is None:
                assert response.json()[key_name] == expected_value, \
                    f"FAILED! Ожидаемое значение {expected_value}!!! Фактическое значение {response.json()[key_name]}"
            else:
                assert response.json()[key_name][field] == expected_value, \
                    f"FAILED! У ключа {response.json()[key_name][field]} фактическое значение {expected_value}"

    @staticmethod
    def checking_big_json(response: Response, key_name: str, expected_value, field=None):
        with allure.step(f"Проверяю что в ответе есть значение {expected_value}"):
            check = response.json()["data"]["request"]
            if field is None:
                assert check.get(key_name) == expected_value, \
                    f"FAILED! Ожидаемое значение {expected_value}!!! Фактическое значение {check.get(key_name)}"
            else:
                assert check.get(key_name)[field] == expected_value, \
                    f"FAILED! У ключа {check.get(key_name)[field]} фактическое значение {expected_value}"

    @staticmethod
    def checking_in_list_json_value(response: Response, key_name, expected_value):
        with allure.step(f"Проверяю что в списке есть значение {expected_value}"):
            for element in response.json():
                assert element[key_name] == expected_value, \
                    f"FAILED! Ожидаемое значение {expected_value}!!! Фактическое значение {element[key_name]}"

    @staticmethod
    def checking_sum_len_lists(old_list: list, new_list: list):
        """Метод проверяет увеличения длинны старого списка и сравнения его с длинной нового списка"""
        with allure.step("Проверяю длины списков"):
            assert len(old_list) + 1 == len(new_list), \
                f"FAILED! Длинна старого списка {len(old_list)} и длинна нового списка {len(new_list)}"

    @staticmethod
    def checking_difference_len_lists(old_list: list, new_list: list):
        """Метод проверяет уменьшения длинны старого списка и сравнения его с длинной нового списка"""
        with allure.step("Проверяю длины списков"):
            assert len(old_list) - 1 == len(new_list), \
                f"FAILED! Длинна старого списка {old_list} и длинна нового списка {new_list}"

    @staticmethod
    def checking_sorted_lists_key(old_list: list, new_list: list, key):
        with allure.step("Сортировка списков и проверка их на равенство"):
            assert sorted(old_list, key=key) == sorted(new_list, key=key), \
                f"FAILED! Старый список {old_list}, Новый список {new_list}"

    @staticmethod
    def check_date_change(calendar_date, number_of_days: int):
        with allure.step(f"Проверка, что дата отправки изменилась на {number_of_days} день/дней"):
            day = datetime.date.today()
            day += datetime.timedelta(days=number_of_days)
            assert calendar_date == str(day), f"{calendar_date} не равна дате {day}"
