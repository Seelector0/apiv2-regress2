from fixture.database import DataBase
import psycopg2


class DataBaseTrackingApi(DataBase):

    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)
        self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)

    def delete_orders_list_in_tracking(self, order_id):
        """Функция чистит таблицу 'public.order'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM "tracking-api".public."order" '
                           f"""WHERE "order".order_id = '{order_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()
