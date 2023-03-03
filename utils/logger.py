from requests import Response
import datetime
import os


class Logger:

    def __init__(self, app):
        self.app = app
        self.file_name = f"{self.app.logs_directory}/log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

    def _write_log_to_file(self, data: str):
        """Метод создаёт файл и записывает в него информацию"""
        with open(self.file_name, mode='a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    def add_request(self, url: str, data: dict, headers: dict, method: str):
        """Метод возвращает и записывает requests"""
        test_name = os.environ.get('PYTEST_CURRENT_TEST')
        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {test_name}\n"
        data_to_add += f"Time: {datetime.datetime.now()}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += "\n"
        self._write_log_to_file(data_to_add)

    def add_response(self, response: Response):
        """Метод возвращает и записывает response"""
        headers_as_dict = dict(response.headers)
        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"X-Trace-Id: {response.request.headers['x-trace-id']}\n"
        data_to_add += "\n-----\n"
        self._write_log_to_file(data_to_add)
