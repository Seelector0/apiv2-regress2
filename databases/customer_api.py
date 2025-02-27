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

    def get_connection_ids(self, shop_ids):
        """Метод собирает (возвращает) список connection_id для каждого shop_id из таблицы 'public.connection'."""
        connection_ids = []
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            for shop_id in shop_ids:
                cursor.execute(f"SELECT id FROM public.connection WHERE shop_id = '{shop_id}'")
                customer_api_rows = cursor.fetchall()
                for row in customer_api_rows:
                    connection_ids.append(row['id'])
        finally:
            cursor.close()
        return connection_ids

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

    def delete_configuration(self, connections_ids):
        r"""Метод чистит таблицу 'public.configuration'.
        :param connections_ids: Список конекшенов в БД.
        """
        cursor = self.database.connection.cursor()
        try:
            counts = 0
            for i in connections_ids:
                cursor.execute(f"DELETE FROM public.configuration WHERE connection_id = '{i}'")
                counts += cursor.rowcount
            cursor.connection.commit()
        finally:
            cursor.close()

