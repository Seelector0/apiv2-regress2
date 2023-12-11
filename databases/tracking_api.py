from fixture.database import DataBase


class DataBaseTrackingApi:

    def __init__(self):
        self.database = DataBase(database="tracking-api")

    def delete_list_orders_in_tracking(self, order_id):
        r"""Функция чистит таблицу 'public.order'.
        :param order_id: ID заказа в БД.
        """
        cursor = self.database.connection.cursor()
        try:
            cursor.execute("""delete from "tracking-api".public."order" """
                           """where "order".order_id = '{order_id}'""".format(order_id=order_id))
            cursor.connection.commit()
        finally:
            cursor.close()
