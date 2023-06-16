

class DataBaseCustomerApi:

    def __init__(self, connections):
        self.customer = connections

    def delete_connection(self, shop_id):
        r"""Функция чистит таблицу 'public.connection'.
        :param shop_id: ID магазина в БД.
        """
        cursor = self.customer.connection_open().cursor()
        try:
            cursor.execute('delete from public.connection '
                           f"""where connection.shop_id = '{shop_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()
