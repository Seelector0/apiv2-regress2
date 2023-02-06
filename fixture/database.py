from environment import ENV_OBJECT
import psycopg2


class DataBase:

    def __init__(self, host, database, user, password):
        """Метод подключения к базе данных"""
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.user_id = ENV_OBJECT.user_id()
        self.db_connections = ENV_OBJECT.db_connections()

    def connection_close(self):
        """Выход из базы данных"""
        self.connection.close()
