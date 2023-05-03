

class DataBaseTrackingApi:

    def __init__(self, tracking):
        self.tracking = tracking

    def delete_orders_list_in_tracking(self, order_id):
        r"""Функция чистит таблицу 'public.order'.
        :param order_id: ID заказа в БД.
        """
        cursor = self.tracking.connection_open().cursor()
        try:
            cursor.execute('DELETE FROM "tracking-api".public."order" '
                           f"""WHERE "order".order_id = '{order_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()
