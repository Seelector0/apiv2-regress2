import os
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Environment:
    LOCAL = "local"
    DEVELOP = "dev"

    URLS = {
        LOCAL: os.getenv("URL_LOCAL"),
        DEVELOP: os.getenv("URL")
    }

    CLIENT_IDS = {
        LOCAL: os.getenv("CLIENT_ID_LOCAL"),
        DEVELOP: os.getenv("CLIENT_ID")
    }

    CLIENT_SECRETS = {
        LOCAL: os.getenv("CLIENT_SECRET_LOCAL"),
        DEVELOP: os.getenv("CLIENT_SECRET")
    }

    ADMIN_IDS = {
        LOCAL: os.getenv("ADMIN_ID"),
        DEVELOP: os.getenv("ADMIN_ID")
    }

    ADMIN_SECRETS = {
        LOCAL: os.getenv("ADMIN_SECRET"),
        DEVELOP: os.getenv("ADMIN_SECRET")
    }

    DATABASE_CONNECTIONS = {
        LOCAL: os.getenv("METASHIP"),
        DEVELOP: os.getenv("CONNECTIONS")
    }

    DATABASE_HOSTS = {
        LOCAL: os.getenv("HOST_LOCAL"),
        DEVELOP: os.getenv("HOST")
    }

    DATABASE_PASSWORDS = {
        LOCAL: os.getenv("DATABASE_PASSWORD_LOCAL"),
        DEVELOP: os.getenv("DATABASE_PASSWORD")
    }

    USER_IDS = {
        LOCAL: os.getenv("USER_ID_LOCAL"),
        DEVELOP: os.getenv("USER_ID")
    }

    CUSTOMERS_IDS = {
        LOCAL: os.getenv("CUSTOMER_ID_LOCAL"),
        DEVELOP: os.getenv("CUSTOMER_ID")
    }

    CUSTOMERS_AGREEMENTS_IDS = {
        LOCAL: os.getenv("CUSTOMER_AGREEMENT_ID_LOCAL"),
        DEVELOP: os.getenv("CUSTOMER_AGREEMENT_ID")
    }
    DEPENDENT_SERVICES_IDS = {
        LOCAL: json.loads(os.getenv('DEPENDENT_SERVICES_LOCAL', '[]')),
        DEVELOP: json.loads(os.getenv('DEPENDENT_SERVICES', '[]'))
    }

    error_massage = "Неизвестное значение переменной ENV:"

    def __init__(self):
        try:
            self.env = os.environ["ENV"]
        except KeyError:
            self.env = self.DEVELOP

    def get_base_url(self):
        """Метод для получения URL для работы за определённым стендом"""
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def client_id(self):
        """Метод для получения client_id для работы за определённым стендом"""
        if self.env in self.CLIENT_IDS:
            return self.CLIENT_IDS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def client_secret(self):
        """Метод для получения client_secret для работы за определённым стендом"""
        if self.env in self.CLIENT_SECRETS:
            return self.CLIENT_SECRETS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def admin_id(self):
        """Метод для получения admin_id для работы за определённым стендом"""
        if self.env in self.ADMIN_IDS:
            return self.ADMIN_IDS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def admin_secret(self):
        """Метод для получения admin_secret для работы за определённым стендом"""
        if self.env in self.ADMIN_SECRETS:
            return self.ADMIN_SECRETS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def db_connections(self):
        """Метод для определения имени базы данных для работы за определённым стендом (connections или metaship)"""
        if self.env in self.DATABASE_CONNECTIONS:
            return self.DATABASE_CONNECTIONS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def host(self):
        """Метод для определения host для базы данных"""
        if self.env in self.DATABASE_HOSTS:
            return self.DATABASE_HOSTS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def password(self):
        """Метод для определения пароля для базы данных"""
        if self.env in self.DATABASE_PASSWORDS:
            return self.DATABASE_PASSWORDS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def user_id(self):
        """Метод для определения user_id для базы данных"""
        if self.env in self.USER_IDS:
            return self.USER_IDS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def customer_id(self):
        """Метод для определения customer_id для работы за определённым стендом"""
        if self.env in self.CUSTOMERS_IDS:
            return self.CUSTOMERS_IDS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def customer_agreements_id(self):
        """Метод для определения customer_agreements_id для работы за определённым стендом"""
        if self.env in self.CUSTOMERS_AGREEMENTS_IDS:
            return self.CUSTOMERS_AGREEMENTS_IDS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def dependent_services(self):
        """Метод для определения зависимых сервисов для работы за определённым стендом"""
        if self.env in self.DEPENDENT_SERVICES_IDS:
            return self.DEPENDENT_SERVICES_IDS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")


ENV_OBJECT = Environment()
