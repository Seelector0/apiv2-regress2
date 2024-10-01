from fixture.database import DataBase
from utils.environment import ENV_OBJECT
from psycopg2.extras import DictCursor
import time


class DataBaseConnections:

    def __init__(self):
        self.database = DataBase(database=ENV_OBJECT.db_connections())

    def close_connection(self):
        self.database.connection.close()

    def delete_cabinet_settings(self):
        """Метод удаляет настройки кабинета из таблицы 'cabinet'"""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(f"""delete from {ENV_OBJECT.db_connections()}.cabinet.setting """
                           f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_shops(self):
        """Метод собирает (возвращает) список магазинов из таблицы 'customer.shop'."""
        db_list_shops = []
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select id from {ENV_OBJECT.db_connections()}.customer.shop """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_shops.append(*row)
        finally:
            cursor.close()
        return db_list_shops

    def delete_list_shops(self):
        """Метод чистит таблицу 'customer.shop'."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.customer.shop """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_list_shops_for_id(self, shop_id):
        """Метод чистит таблицу 'customer.shop'."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.customer.shop """
                                 f"""where id = '{shop_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_warehouses(self):
        """Метод собирает (возвращает) список складов из таблицы 'customer.warehouse'."""
        db_list_warehouses = []
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select id from {ENV_OBJECT.db_connections()}.customer.warehouse """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_warehouses.append(*row)
        finally:
            cursor.close()
        return db_list_warehouses

    def get_list_warehouses_value(self, warehouse_id: str, value: str):
        """Метод возвращает удален склад или нет (True - удалён, False - нет)"""
        db_list_warehouses = []
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select {value} from {ENV_OBJECT.db_connections()}.customer.warehouse """
                                 f"""where id = '{warehouse_id}' and user_id = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_warehouses.append(*row)
        finally:
            cursor.close()
        return db_list_warehouses

    def delete_list_warehouses(self):
        """Метод чистит таблицу 'customer.warehouse'."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.customer.warehouse """
                                 f"""where warehouse.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_list_warehouses_for_id(self, warehouse_id):
        """Метод чистит таблицу 'customer.warehouse'."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.customer.warehouse """
                                 f"""where id = '{warehouse_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_list_delivery_services(self):
        """Метод чисти таблицу 'customer.credential'."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.customer.credential """
                                 f"""where credential.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_list_drafts(self):
        """Метод чистит таблицу 'order.draft'."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".draft """
                                 f"""where draft.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_orders(self):
        """Метод собирает (возвращает) id всех заказов из таблицы order."""
        db_list_order = []
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select id from {ENV_OBJECT.db_connections()}."order"."order" """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_order.append(*row)
        finally:
            cursor.close()
        return db_list_order

    def get_list_all_orders_out_parcel(self):
        """Метод собирает (возвращает) список заказов который не удалены из таблицы order."""
        db_list_order = []
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select id from {ENV_OBJECT.db_connections()}."order"."order" """
                                 f"""where state='succeeded' and deleted=false and user_id='{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_order.append(*row)
        finally:
            cursor.close()
        return db_list_order

    def get_list_all_orders_in_parcel(self):
        """Метод собирает (возвращает) список заказов из таблицы order_parcel"""
        db_list_orders_in_parcel = []
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select order_id from {ENV_OBJECT.db_connections()}."order".order_parcel """
                                 f"""where deleted=false and parcel_id = '{self.get_list_parcels()[0]}'""")
            for row in cursor:
                db_list_orders_in_parcel.append(*row)
        finally:
            cursor.close()
        return db_list_orders_in_parcel

    def get_list_all_orders_in_parcel_for_parcel_id(self, parcel_id):
        """Метод собирает (возвращает) список заказов из таблицы order_parcel с возможностью передачи номера партии"""
        db_list_orders_in_parcel = []
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select order_id from {ENV_OBJECT.db_connections()}."order".order_parcel """
                                 f"""where deleted=false and parcel_id = '{parcel_id}'""")
            for row in cursor:
                db_list_orders_in_parcel.append(*row)
        finally:
            cursor.close()
        return db_list_orders_in_parcel

    def get_list_order_value(self, order_id: str, value: str):
        r"""Метод возвращает значения поля.
        :param order_id: ID заказа.
        :param value: Поле в БД.
        """
        db_list_order_id = []
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""select {value} from {ENV_OBJECT.db_connections()}."order"."order" """
                                 f"""where id='{order_id}' and user_id='{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_order_id.append(*row)
        finally:
            cursor.close()
        return db_list_order_id

    def wait_create_order(self, order_id: str):
        r"""Метод ждёт загрузки заказа по его id.
        :param order_id: ID заказа.
        """
        value = self.get_list_order_value(order_id=order_id, value="state")
        counter = 0
        while str(*value) != "succeeded" and counter < 50:
            time.sleep(1)
            value = self.get_list_order_value(order_id=order_id, value="state")
            counter += 1
            if str(*value) in ["succeeded", "failed"]:
                break

    def delete_list_orders(self):
        """Метод чистит таблицу order."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order"."order" """
                                 f"""where "order".user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_list_orders_for_shop(self, shop_id):
        """Метод чистит таблицу order по shop_id."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order"."order" 
            where "order".user_id = '{ENV_OBJECT.user_id()}' and data::text LIKE '%{shop_id}%'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_parcels(self):
        """Метод собирает (возвращает) список id партий из таблицы parcel."""
        db_list_parcel = []
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select id from {ENV_OBJECT.db_connections()}."order".parcel """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_parcel.append(*row)
        finally:
            cursor.close()
        return db_list_parcel

    def delete_list_parcels(self):
        """Метод чистит таблицу parcel."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".parcel """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_list_parcels_for_id(self, parcel_id):
        """Метод чистит таблицу parcel по id партии."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".parcel """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}' and id='{parcel_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_failed_parcel(self):
        """Метод чистит таблицу failed_parcel."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".failed_parcel """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_order_document(self, order_id: str):
        r"""Метод чистит таблицу 'order.order_document'.
        :param order_id: ID заказа в БД.
        """
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".order_document """
                                 f"""where order_document.order_id = '{order_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_order_parcel(self, parcel_id: str):
        r"""Метод чистит таблицу 'order.order_parcel'.
        :param parcel_id: ID партии в БД.
        """
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".order_parcel """
                                 f"""where order_parcel.parcel_id = '{parcel_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_order_path(self):
        """Метод чистит таблицу 'order.order_path'."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".order_patch """
                                 f"""where order_patch.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_intakes_value(self, intake_id: str, value):
        """Метод возвращает список поля из таблицы intakes."""
        db_list_intakes = []
        cursor = self.database.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select {value} from {ENV_OBJECT.db_connections()}.intake.intake """
                                 f"""where id = '{intake_id}' and user_id = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_intakes.append(*row)
        finally:
            cursor.close()
        return db_list_intakes

    def delete_intakes(self):
        """Метод чистит таблицу 'intake.intake'."""
        cursor = self.database.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.intake.intake """
                                 f"""where intake.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_all_setting(self):
        """Метод чистит все таблицы."""
        self.delete_cabinet_settings()
        self.delete_list_shops()
        self.delete_list_warehouses()
        self.delete_list_delivery_services()
        self.delete_list_drafts()
        for id_ in self.get_list_all_orders_out_parcel():
            self.delete_order_document(order_id=id_)
        self.delete_list_orders()
        for id_ in self.get_list_parcels():
            self.delete_order_parcel(parcel_id=id_)
        self.delete_order_path()
        self.delete_list_parcels()
        self.delete_failed_parcel()
        self.delete_intakes()
