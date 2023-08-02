

class DataBaseTrackingApi:

    def __init__(self, tracking):
        self.tracking = tracking

    def delete_list_orders_in_tracking(self, order_id):
        r"""Функция чистит таблицу 'public.order'.
        :param order_id: ID заказа в БД.
        """
        cursor = self.tracking.connection_open().cursor()
        try:
            cursor.execute("""delete from "tracking-api".public."order" """
                           """where "order".order_id = '{order_id}'""".format(order_id=order_id))
            cursor.connection.commit()
        finally:
            cursor.close()
