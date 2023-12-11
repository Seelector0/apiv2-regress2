from environment import ENV_OBJECT
import psycopg2


class DataBase:

    def __init__(self, database):
        self.connection = psycopg2.connect(host=ENV_OBJECT.host(), database=database, user=ENV_OBJECT.db_connections(),
                                           password=ENV_OBJECT.password())
