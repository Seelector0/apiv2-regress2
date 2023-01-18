from fixture.database import DataBase
import psycopg2


class DataBaseCustomerApi(DataBase):

    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)
        self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)

    def delete_connection(self, shop_id):
        """Функция чистит таблицу 'public.connection'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM public.connection '
                           f"""WHERE connection.shop_id = '{shop_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()
