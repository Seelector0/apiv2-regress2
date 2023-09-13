from environment import ENV_OBJECT
import psycopg2


class DataBaseTrackingApi:

    def __init__(self):
        self.connection = psycopg2.connect(host=ENV_OBJECT.host(), database=ENV_OBJECT.db_tracking_api(),
                                           user=ENV_OBJECT.db_connections(), password=ENV_OBJECT.password())

    def delete_list_orders_in_tracking(self, order_id):
        r"""Функция чистит таблицу 'public.order'.
        :param order_id: ID заказа в БД.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute("""delete from "tracking-api".public."order" """
                           """where "order".order_id = '{order_id}'""".format(order_id=order_id))
            cursor.connection.commit()
        finally:
            cursor.close()
