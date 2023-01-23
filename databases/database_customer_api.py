from fixture.database import DataBase


class DataBaseCustomerApi(DataBase):

    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)

    def delete_connection(self, shop_id):
        """Функция чистит таблицу 'public.connection'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM public.connection '
                           f"""WHERE connection.shop_id = '{shop_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()
