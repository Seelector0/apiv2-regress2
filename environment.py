from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())


class Environment:

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
        DEVELOP: f"{os.getenv('USER_LOACL')}"
    }

    DATABASE_PASSWORDS = {
        LOCAL: f"{os.getenv('DATABASE_PASSWORD_LOCAL')}",
        DEVELOP: f"{os.getenv('DATABASE_PASSWORD')}"
    }

    DATABASE_USER_IDS = {
        LOCAL: f"{os.getenv('USER_ID_LOCAL')}",
        DEVELOP: f"{os.getenv('USER_ID')}"
    }

    def __init__(self):
        try:
            self.env = os.environ['ENV']
        except KeyError:
            self.env = self.DEVELOP

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"Неизвестное значение переменной ENV {self.env}")


ENV_OBJECT = Environment()
