from databases.customer_api import DataBaseCustomerApi
from databases.tracking_api import DataBaseTrackingApi
from databases.connections import DataBaseConnections
from databases.widget_api import DataBaseWidgetApi
from environment import ENV_OBJECT
import psycopg2


class DataBase:

    def __init__(self, database: str = None):
        self.database = database
        self.host = ENV_OBJECT.host()
        self.user = ENV_OBJECT.db_connections()
        self.password = ENV_OBJECT.password()
        self.user_id = ENV_OBJECT.user_id()
        self.db_connections = ENV_OBJECT.db_connections()
        self.db_customer = ENV_OBJECT.db_customer_api()
        self.db_tracking = ENV_OBJECT.db_tracking_api()
        self.db_widget = ENV_OBJECT.db_widget_api()
        self.connection = None
        self.metaship = DataBaseConnections(self)
        self.customer = DataBaseCustomerApi(self)
        self.tracking = DataBaseTrackingApi(self)
        self.widget = DataBaseWidgetApi(self)

    def connection_open(self):
        """Метод подключение к БД"""
        self.connection = psycopg2.connect(host=self.host, database=self.database,
                                           user=self.user, password=self.password)
        return self.connection

    def connection_close(self):
        """Метод закрытия подключения к БД"""
        self.connection_open().close()
