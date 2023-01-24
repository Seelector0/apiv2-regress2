from requests import Response
import allure
import json
import os


class Checking:

    @staticmethod
    def check_status_code(response: Response, expected_status_code: int):
        """Метод для проверки статус кода"""
        with allure.step("Проверяю что статус код равен заданному"):
            assert response.status_code == expected_status_code, \
                f"Не ожидаемый status code! Ожидаемый: {expected_status_code}. Фактический: {response.status_code}"

    @staticmethod
    def checking_json_key(response: Response, expected_value: list):
        """Метод для проверки обязательных полей (ключей) в ответе"""
        with allure.step("Проверяю что в ответе есть ключи (key)"):
            token = json.loads(response.text)
            assert list(token) == expected_value, \
                f"Не ожидаемые ключи! Ожидаемые {list(token)}. Фактические {expected_value}"

    @staticmethod
    def checking_json_value(response: Response, key_name: str, expected_value, field = None):
        """Метод для проверки обязательных полей (значений) в ответе"""
        with allure.step("Проверяю что в ответе есть значение (value)"):
            check = response.json()
            if field is None:
                assert check.get(key_name) == expected_value, \
                    f"FAILED! У ключа {check.get(key_name)} фактическое значение {expected_value}"
            else:
                assert check.get(key_name)[field] == expected_value, \
                    f"FAILED! У ключа {check.get(key_name)[field]} фактическое значение {expected_value}"

    @staticmethod
    def checking_sum_len_lists(old_list: list, new_list: list):
        """Метод проверяет увеличения длинны старого списка и сравнения его с длинной нового списка"""
        with allure.step("Проверяю длины списков"):
            assert len(old_list) + 1 == len(new_list), \
                f"FAILED! Длинна старого списка {old_list} и длинна нового списка {new_list}"

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
    def download_file_false(directory, file):
        with allure.step("Проверяю что данного файла нет в директории"):
            assert os.path.exists(f"{directory}/{file}") is False

    @staticmethod
    def download_file_true(directory, file):
        with allure.step("Проверяю что данного файла есть в директории"):
            assert os.path.exists(f"{directory}/{file}") is True

