from fixture.database import DataBase
from environment import ENV_OBJECT
from psycopg2.extras import DictCursor


class DataBaseCustomerApi(DataBase):

    def __init__(self):
        super().__init__(database=ENV_OBJECT.db_customer_api())
        self.customer_agreements_id = ENV_OBJECT.customer_agreements_id()

    def get_connections_id(self, shop_id):
        r"""Метод получения connection_id из БД.
        :param shop_id: ID магазина в БД.
        """
        db_list_connection_id = []
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query="""select id from "customer-api".public.connection """
                                 """where connection.shop_id = '{shop_id}'""".format(shop_id=shop_id))
            for row in cursor:
                db_list_connection_id.append(*row)
        finally:
            cursor.close()
        return db_list_connection_id

    def delete_connection(self, shop_id):
        r"""Метод чистит таблицу 'public.connection'.
        :param shop_id: ID магазина в БД.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query="""delete from "customer-api".public.connection """
                                 """where connection.shop_id = '{shop_id}'""".format(shop_id=shop_id))
            cursor.connection.commit()
        finally:
            cursor.close()
