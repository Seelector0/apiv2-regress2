from fixture.database import DataBase


class DataBaseCustomerApi(DataBase):

    def delete_connection(self, shop_id):
        r"""Функция чистит таблицу 'public.connection'.
        :param shop_id: ID магазина в БД.
        """
        cursor = self.connection_open().cursor()
        try:
            cursor.execute('DELETE FROM public.connection '
                           f"""WHERE connection.shop_id = '{shop_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()
