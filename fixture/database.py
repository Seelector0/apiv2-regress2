from environment import ENV_OBJECT
import psycopg2


class DataBase:

    def __init__(self, database: str):
        self.user_id = ENV_OBJECT.user_id()
        self.db_name = ENV_OBJECT.db_connections()
        self.connection = psycopg2.connect(host=ENV_OBJECT.host(), database=database, user=self.db_name,
                                           password=ENV_OBJECT.password())
