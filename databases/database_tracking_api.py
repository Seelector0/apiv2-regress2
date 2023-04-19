from fixture.database import DataBase


class DataBaseTrackingApi(DataBase):

    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)

    def delete_orders_list_in_tracking(self, order_id):
        r"""Функция чистит таблицу 'public.order'.
        :param order_id: ID заказа в БД.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM "tracking-api".public."order" '
                           f"""WHERE "order".order_id = '{order_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()
