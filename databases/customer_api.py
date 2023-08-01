from psycopg2.extras import DictCursor


class DataBaseCustomerApi:

    def __init__(self, customer_api):
        self.customer_api = customer_api

    def get_connections_id(self, shop_id):
        r"""Метод получения connection_id из БД.
        :param shop_id: ID магазина в БД.
        """
        db_list_connection_id = []
        cursor = self.customer_api.connection_open().cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query="""select id from "customer-api".public.connection """
                                 f"""where connection.shop_id = '{shop_id}'""")
            for row in cursor:
                db_list_connection_id.append(*row)
        finally:
            cursor.close()
        return db_list_connection_id

    def delete_connection(self, shop_id):
        r"""Метод чистит таблицу 'public.connection'.
        :param shop_id: ID магазина в БД.
        """
        cursor = self.customer_api.connection_open().cursor()
        try:
            cursor.execute("""delete from "customer-api".public.connection """
                           f"""where connection.shop_id = '{shop_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()
