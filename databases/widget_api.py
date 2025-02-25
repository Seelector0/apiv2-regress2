from fixture.database import DataBase
from utils.environment import ENV_OBJECT


class DataBaseWidgetApi:

    def __init__(self):
        self.database = DataBase(database="widget-api")

    def delete_widgets_id(self):
        r"""Функция чистит таблицу '"widget-api".public.credentials'.
        """
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(f"""delete from "widget-api".public.credentials """
                           f"""where credentials.customer_id = '{ENV_OBJECT.customer_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()
