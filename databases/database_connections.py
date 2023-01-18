from fixture.database import DataBase
from model.warehouses import Warehouse
from model.orders import Order
from model.parcels import Parcel
from model.shops import Shop
import psycopg2


class DataBaseConnections(DataBase):

    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)
        self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.user_id = "3172df65-83b6-4a02-aa2c-7a4ae5297ed6"

    def delete_cabinet_settings(self):
        """Функция удаляет настройки кабинета из таблицы 'cabinet'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM connections.cabinet.setting "
                           f"""WHERE setting.user_id = '{self.user_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_shops_list(self):
        """Функция собирает (возвращает) список магазинов из таблицы 'customer.shop'"""
        db_list_shop = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT name, id FROM connections.customer.shop "
                           f"""WHERE shop.user_id = '{self.user_id}'""")
            for row in cursor:
                (name, shop_id) = row
                db_list_shop.append(Shop(shop_name=name, shop_id=shop_id))
        finally:
            cursor.close()
        return db_list_shop

    def delete_shops_list(self):
        """Функция чистит таблицу 'customer.shop'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM connections.customer.shop "
                           f"WHERE shop.user_id = '{self.user_id}'")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_warehouses_list(self):
        """Функция собирает (возвращает) список складов из таблицы 'customer.warehouse'"""
        db_list_warehouse = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT name, id FROM connections.customer.warehouse "
                           f"""WHERE warehouse.user_id = '{self.user_id}'""")
            for row in cursor:
                (name, warehouse_id) = row
                db_list_warehouse.append(Warehouse(name_warehouse=name, warehouse_id=warehouse_id))
        finally:
            cursor.close()
        return db_list_warehouse

    def delete_warehouses_list(self):
        """Функция чистит таблицу 'customer.warehouse'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM connections.customer.warehouse "
                           f"WHERE warehouse.user_id = '{self.user_id}'")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_delivery_services_list(self):
        """Функция собирает (возвращает) список подключенных служб доставок из таблицы 'customer.credential'"""
        db_list_delivery_service = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT order_id, type FROM connections.customer.credential"
                           f"""WHERE customer.shop.user_id = '{self.user_id}'""")
        finally:
            cursor.close()
        return db_list_delivery_service

    def delete_delivery_services_list(self):
        """Функция чисти таблицу 'customer.credential'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM connections.customer.credential "
                           f"WHERE credential.user_id = '{self.user_id}'")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_drafts_list(self):
        """Функция собирает (возвращает) список черновиков из таблицы 'order.draft'"""
        db_list_order = []
        cursor = self.connection.cursor()
        try:
            cursor.execute('SELECT id FROM connections."order".draft '
                           f"""WHERE draft.user_id = = '{self.user_id}'""")
            for row in cursor:
                (order_id, shop_number) = row
                db_list_order.append(Order(order_id=order_id, shop_number=shop_number))
        finally:
            cursor.close()
        return db_list_order

    def delete_drafts_list(self):
        """Функция чистит таблицу 'order.draft'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM connections."order".draft '
                           f"""WHERE draft.user_id = '{self.user_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_orders_list(self):
        """Функция собирает (возвращает) список заказов из таблицы 'order.order'"""
        db_list_order = []
        cursor = self.connection.cursor()
        try:
            cursor.execute('SELECT id, shop_number FROM connections."order"."order" '
                           f"""WHERE "order".user_id = '{self.user_id}'""")
            for row in cursor:
                (order_id, shop_number) = row
                db_list_order.append(Order(order_id=order_id, shop_number=shop_number))
        finally:
            cursor.close()
        return db_list_order

    def delete_orders_list(self):
        """Функция чистит таблицу 'order.order'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM connections."order"."order" '
                           f"""WHERE "order".user_id = '{self.user_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_parcels_list(self):
        """Функция собирает (возвращает) список партий из таблицы 'order.parcel'"""
        db_list_parcel = []
        cursor = self.connection.cursor()
        try:
            cursor.execute('SELECT id, SUBSTRING(rid, 3) FROM connections."order".parcel '
                           f"""WHERE parcel.user_id = '{self.user_id}'""")
            for row in cursor:
                (parcel_id, rid) = row
                db_list_parcel.append(Parcel(parcel_id=parcel_id, rid=rid))
        finally:
            cursor.close()
        return db_list_parcel

    def delete_parcels_list(self):
        """Функция чистит таблицу 'order.parcel'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM connections."order".parcel '
                           f"""WHERE parcel.user_id = '{self.user_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_order_document(self, order_id):
        """Функция чистит таблицу 'order.order_document'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM connections."order".order_document '
                           f"""WHERE order_document.order_id = '{order_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_order_parcel(self, parcel_id):
        """Функция чистит таблицу 'order.order_parcel'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM connections."order".order_parcel '
                           f"""WHERE order_parcel.parcel_id = '{parcel_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_order_path(self):
        """Функция чистит таблицу 'order.order_path'"""
        cursor = self.connection.cursor()
        try:
            cursor.execute('DELETE FROM connections."order".order_patch '
                           f"""WHERE order_patch.user_id = '{self.user_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_all_setting(self):
        """Функция удаляет всё выше перечисленное"""
        self.delete_cabinet_settings()
        self.delete_shops_list()
        self.delete_warehouses_list()
        self.delete_delivery_services_list()
        self.delete_drafts_list()
        orders: list = self.get_orders_list()
        for i in orders:
            self.delete_order_document(order_id=i.order_id)
        self.delete_orders_list()
        parcels: list = self.get_parcels_list()
        for i in parcels:
            self.delete_order_parcel(parcel_id=i.parcel_id)
        self.delete_order_path()
        self.delete_parcels_list()
