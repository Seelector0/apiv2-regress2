"""Метод подключения к базе данных."""


class DataBase:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connection_close(self):
        """Выход из базы данных"""
        self.connection.close()
