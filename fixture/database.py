from databases.database_connections import DataBaseConnections
from databases.database_customer_api import DataBaseCustomerApi
from databases.database_tracking_api import DataBaseTrackingApi
from environment import ENV_OBJECT
import psycopg2


class DataBase:

    def __init__(self, database=None):
        self.database = database
        self.host = ENV_OBJECT.host()
        self.user = ENV_OBJECT.db_connections()
        self.password = ENV_OBJECT.password()
        self.user_id = ENV_OBJECT.user_id()
        self.db_connections = ENV_OBJECT.db_connections()
        self.connection = None
        self.metaship = DataBaseConnections(self)
        self.customer = DataBaseCustomerApi(self)
        self.tracking = DataBaseTrackingApi(self)

    def connection_open(self):
        """Метод подключение к БД"""
        self.connection = psycopg2.connect(host=self.host, database=self.database,
                                           user=self.user, password=self.password)
        return self.connection

    def connection_close(self):
        """Метод закрытия подключения к БД"""
        self.connection_open().close()
