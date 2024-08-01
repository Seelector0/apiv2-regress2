from fixture.database import DataBase
from psycopg2.extras import DictCursor


class DataBaseCustomerApi:

    def __init__(self):
        self.database = DataBase(database="customer-api")

    def close_connection(self):
        self.database.connection.close()

    def get_connections_id(self, shop_id, delivery_service):
        r"""Метод получения connection_id из БД.
        :param shop_id: ID магазина в БД.
        :param delivery_service: Название СД.
        """
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute("""
                        SELECT id FROM "customer-api".public.connection 
                        WHERE shop_id = '{shop_id}' AND delivery_service = '{delivery_service}'
                        """.format(shop_id=shop_id, delivery_service=delivery_service))

            row = cursor.fetchone()
            if row:
                connection_id = row['id']
            else:
                connection_id = None
        finally:
            cursor.close()

        return connection_id

    def delete_connection(self, shop_id):
        r"""Метод чистит таблицу 'public.connection'.
        :param shop_id: ID магазина в БД.
        """
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query="""delete from "customer-api".public.connection """
                                 """where connection.shop_id = '{shop_id}'""".format(shop_id=shop_id))
            cursor.connection.commit()
        finally:
            cursor.close()
