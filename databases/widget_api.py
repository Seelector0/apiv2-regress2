from environment import ENV_OBJECT
from psycopg2.extras import DictCursor
import psycopg2


class DataBaseWidgetApi:

    def __init__(self):
        self.connection = psycopg2.connect(host=ENV_OBJECT.host(), database="widget-api",
                                           user=ENV_OBJECT.db_connections(), password=ENV_OBJECT.password())

    def get_widgets_id(self, shop_id):
        r"""Метод получения widget_id из БД.
        :param shop_id: ID магазина в БД.
        """
        list_widget_id = []
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query="""select id from "widget-api".public.credentials """
                                 """where credentials.shop_id = '{shop_id}'""".format(shop_id=shop_id))
            for row in cursor:
                list_widget_id.append(*row)
        finally:
            cursor.close()
        return list_widget_id

    def delete_widgets_id(self, shop_id):
        r"""Функция чистит таблицу '"widget-api".public.credentials'.
        :param shop_id: ID магазина в БД.
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query="""delete from "widget-api".public.credentials """
                                 """where credentials.shop_id = '{shop_id}'""".format(shop_id=shop_id))
            cursor.connection.commit()
        finally:
            cursor.close()
