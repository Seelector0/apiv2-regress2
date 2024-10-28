import inspect
import os

import pytest


def get_caller_info():
    """Возвращает имя вызывающей функции и имя файла."""
    caller_frame = inspect.stack()[3]
    caller_function = caller_frame.function
    caller_filename = os.path.basename(caller_frame.filename)
    return caller_function, caller_filename


def check_shared_data(shared_data, key=None):
    """Функция для проверки shared_data и пропуска теста."""
    if not shared_data:
        caller_function, caller_filename = get_caller_info()
        pytest.skip(f"В файле '{caller_filename}'тест '{caller_function}' пропущен: "
                    "Список shared_data пуст, невозможно выполнить тест.")
    if key and not shared_data.get(key):
        caller_function, caller_filename = get_caller_info()
        pytest.skip(f"В файле '{caller_filename}'тест '{caller_function}' пропущен: "
                    f"Список '{key}' в 'shared_data' пуст, невозможно выполнить тест.")

