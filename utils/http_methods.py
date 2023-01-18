from dotenv import load_dotenv, find_dotenv
from utils.logger import Logger
import requests
import allure
import os


load_dotenv(find_dotenv())


class HttpMethods:

    @staticmethod
    def get(link: str, data=None, headers: dict = None):
        with allure.step(f"GET requests to URL '{link}'"):
            return HttpMethods._send(link, data, headers, 'GET')

    @staticmethod
    def post(link: str, data=None, headers: dict = None):
        with allure.step(f"POST requests to URL '{link}'"):
            return HttpMethods._send(link, data, headers, 'POST')

    @staticmethod
    def patch(link: str, data=None, headers: dict = None):
        with allure.step(f"POST requests to URL '{link}'"):
            return HttpMethods._send(link, data, headers, 'PATCH')

    @staticmethod
    def put(link: str, data=None, headers: dict = None):
        with allure.step(f"PUT requests to URL '{link}'"):
            return HttpMethods._send(link, data, headers, 'PUT')

    @staticmethod
    def delete(link: str, data=None, headers: dict = None):
        with allure.step(f"DELETE requests to URL '{link}'"):
            return HttpMethods._send(link, data, headers, 'DELETE')

    @staticmethod
    def _send(link: str, data, headers: dict, method: str):
        link = f"{os.getenv('URL')}/v2{link}"
        if headers is None:
            headers = {}
        # Logger.add_request(link, data, headers, method)
        if method == 'GET':
            response = requests.get(url=link, params=data, headers=headers)
        elif method == 'POST':
            response = requests.post(url=link, data=data, headers=headers)
        elif method == 'PATCH':
            response = requests.patch(url=link, data=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(url=link, data=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url=link, data=data, headers=headers)
        else:
            raise Exception(f"Получен неверный HTTP метод '{method}'")
        # Logger.add_response(response)
        return response
