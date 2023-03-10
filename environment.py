from dotenv import load_dotenv, find_dotenv
import os


class Environment:

    load_dotenv(find_dotenv())

    LOCAL = 'local'
    DEVELOP = 'dev'

    URLS = {
        LOCAL: f"{os.getenv('URL_LOCAL')}",
        DEVELOP: f"{os.getenv('URL')}"
    }

    CLIENT_IDS = {
        LOCAL: f"{os.getenv('CLIENT_ID_LOCAL')}",
        DEVELOP: f"{os.getenv('CLIENT_ID')}"
    }

    CLIENT_SECRETS = {
        LOCAL: f"{os.getenv('CLIENT_SECRET_LOCAL')}",
        DEVELOP: f"{os.getenv('CLIENT_SECRET')}"
    }

    DATABASE_CONNECTIONS = {
        LOCAL: f"{os.getenv('CONNECTIONS_LOCAL')}",
        DEVELOP: f"{os.getenv('CONNECTIONS')}"
    }

    DATABASE_CUSTOMER_API = {
        LOCAL: f"{os.getenv('CUSTOMER_API_LOCAL')}",
        DEVELOP: f"{os.getenv('CUSTOMER_API')}"
    }

    DATABASE_TRACKING_API = {
        LOCAL: f"{os.getenv('TRACKING_API_LOCAL')}",
        DEVELOP: f"{os.getenv('TRACKING_API')}"
    }

    DATABASE_HOSTS = {
        LOCAL: f"{os.getenv('HOST_LOCAL')}",
        DEVELOP: f"{os.getenv('HOST')}"
    }

    DATABASE_USERS = {
        LOCAL: f"{os.getenv('USER')}",
        DEVELOP: f"{os.getenv('USER_LOCAL')}"
    }

    DATABASE_PASSWORDS = {
        LOCAL: f"{os.getenv('DATABASE_PASSWORD_LOCAL')}",
        DEVELOP: f"{os.getenv('DATABASE_PASSWORD')}"
    }

    USER_IDS = {
        LOCAL: f"{os.getenv('USER_ID_LOCAL')}",
        DEVELOP: f"{os.getenv('USER_ID')}"
    }

    error_massage = "Неизвестное значение переменной ENV:"

    def __init__(self):
        try:
            self.env = os.environ['ENV']
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

    def db_customer_api(self):
        """Метод для определения имени базы данных для работы за определённым стендом (customer-api)"""
        if self.env in self.DATABASE_CUSTOMER_API:
            return self.DATABASE_CUSTOMER_API[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def db_connections(self):
        """Метод для определения имени базы данных для работы за определённым стендом (connections или metaship)"""
        if self.env in self.DATABASE_CONNECTIONS:
            return self.DATABASE_CONNECTIONS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def db_tracking_api(self):
        if self.env in self.DATABASE_TRACKING_API:
            """Метод для определения имени базы данных для работы за определённым стендом (tracking-api)"""
            return self.DATABASE_TRACKING_API[self.env]
        else:
            raise Exception(f"{self.error_massage} {self.env}")

    def host(self):
        """Метод для определения host для базы данных"""
        if self.env in self.DATABASE_HOSTS:
            return self.DATABASE_HOSTS[self.env]
        else:
            raise Exception(f"{Environment.error_massage} {self.env}")

    def user(self):
        """Метод для определения user для базы данных"""
        if self.env in self.DATABASE_USERS:
            return self.DATABASE_USERS[self.env]
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


ENV_OBJECT = Environment()
