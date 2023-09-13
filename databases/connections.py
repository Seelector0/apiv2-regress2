from environment import ENV_OBJECT
from psycopg2.extras import DictCursor
import psycopg2
import time
import json


class DataBaseConnections:

    def __init__(self):
        self.connection = psycopg2.connect(host=ENV_OBJECT.host(), database=ENV_OBJECT.db_connections(),
                                           user=ENV_OBJECT.db_connections(), password=ENV_OBJECT.password())

    def get_list_shops(self):
        """Метод собирает (возвращает) список магазинов из таблицы 'customer.shop'."""
        db_list_shops = []
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select id from {ENV_OBJECT.db_connections()}.customer.shop """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_shops.append(*row)
        finally:
            cursor.close()
        return db_list_shops

    def get_list_shops_value(self, shop_id: str, value: str):
        """Метод возвращает список поля из БД."""
        db_list_shops = []
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select {value} from {ENV_OBJECT.db_connections()}.customer.shop """
                                 f"""where id = '{shop_id}' and user_id = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_shops.append(*row)
        finally:
            cursor.close()
        return db_list_shops

    def delete_list_shops(self):
        """Метод чистит таблицу 'customer.shop'."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.customer.shop """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_warehouses(self):
        """Метод собирает (возвращает) список складов из таблицы 'customer.warehouse'."""
        db_list_warehouses = []
        cursor = self.connection.cursor(cursor_factory=DictCursor)
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
        cursor = self.connection.cursor(cursor_factory=DictCursor)
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
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.customer.warehouse """
                                 f"""where warehouse.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_delivery_services(self):
        """Метод собирает (возвращает) список подключенных служб доставок из таблицы 'customer.credential'"""
        db_list_delivery_service = []
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""select id from {ENV_OBJECT.db_connections()}.customer.credential """
                                 f"""where customer.shop.user_id = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_delivery_service.append(*row)
        finally:
            cursor.close()
        return db_list_delivery_service

    def delete_list_delivery_services(self):
        """Метод чисти таблицу 'customer.credential'."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.customer.credential """
                                 f"""where credential.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_drafts(self):
        """Метод собирает (возвращает) список черновиков из таблицы 'order.draft'."""
        db_list_drafts = []
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select id from {ENV_OBJECT.db_connections()}."order".draft """
                                 f"""where draft.user_id = = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_drafts.append(*row)
        finally:
            cursor.close()
        return db_list_drafts

    def delete_list_drafts(self):
        """Метод чистит таблицу 'order.draft'."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".draft """
                                 f"""where draft.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_orders(self):
        """Метод собирает (возвращает) id всех заказов из таблицы order."""
        db_list_order = []
        cursor = self.connection.cursor(cursor_factory=DictCursor)
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
        cursor = self.connection.cursor(cursor_factory=DictCursor)
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
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select order_id from {ENV_OBJECT.db_connections()}."order".order_parcel """
                                 f"""where deleted=false and parcel_id = '{self.get_list_parcels()[0]}'""")
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
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""select {value} from {ENV_OBJECT.db_connections()}."order"."order" """
                                 f"""where id='{order_id}' and user_id='{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_order_id.append(*row)
        finally:
            cursor.close()
        return db_list_order_id

    def get_order_id_from_database(self, not_in_parcel: bool = None, in_parcel: bool = None, single_order: bool = None,
                                   multy_order: bool = None):
        r"""Метод получения id заказов.
        :param not_in_parcel: Все заказы не в партии.
        :param in_parcel: Все заказы в партии.
        :param single_order: Одноместные заказы.
        :param multy_order: Многоместные заказы.
        """
        order_id = None
        list_orders = None
        db_list_data = []
        db_list_single_order_id = []
        db_list_multy_order_id = []
        cursor = self.connection.cursor()
        if in_parcel:
            list_orders = self.get_list_all_orders_in_parcel()
        elif not_in_parcel:
            list_orders = self.get_list_all_orders_out_parcel()
        try:
            for order_id in list_orders:
                cursor.execute(query=f"""select data from {ENV_OBJECT.db_connections()}."order"."order" """
                                     f"""where id='{order_id}' and state='succeeded' and deleted=false """
                                     f"""and user_id='{ENV_OBJECT.user_id()}'""")
                for row in cursor:
                    db_list_data.append(*row)
            for i in db_list_data:
                if len(json.loads(i["request"].replace('\"', '"'))["places"]) == 1:
                    db_list_single_order_id.append(order_id)
                elif len(json.loads(i["request"].replace('\"', '"'))["places"]) > 1:
                    db_list_multy_order_id.append(order_id)
        finally:
            cursor.close()
        if single_order:
            return db_list_single_order_id
        if multy_order:
            return db_list_multy_order_id

    def wait_create_order(self, order_id: str):
        r"""Метод ждёт загрузки заказа по его id.
        :param order_id: ID заказа.
        """
        value = self.get_list_order_value(order_id=order_id, value="state")
        counter = 0
        while str(*value) != "succeeded" and counter < 120:
            time.sleep(1)
            value = self.get_list_order_value(order_id=order_id, value="state")
            counter += 1
            if str(*value) in ["succeeded", "failed"]:
                break

    def delete_list_orders(self):
        """Метод чистит таблицу order."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order"."order" """
                                 f"""where "order".user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_parcels(self):
        """Метод собирает (возвращает) список id партий из таблицы parcel."""
        db_list_parcel = []
        cursor = self.connection.cursor(cursor_factory=DictCursor)
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
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".parcel """
                                 f"""where user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_failed_parcel(self):
        """Метод чистит таблицу failed_parcel."""
        cursor = self.connection.cursor()
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
        cursor = self.connection.cursor()
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
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".order_parcel """
                                 f"""where order_parcel.parcel_id = '{parcel_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_order_path(self):
        """Метод чистит таблицу 'order.order_path'."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}."order".order_patch """
                                 f"""where order_patch.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_intakes_value(self, intake_id: str, value):
        """Метод возвращает список поля из таблицы intakes."""
        db_list_intakes = []
        cursor = self.connection.cursor(cursor_factory=DictCursor)
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
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.intake.intake """
                                 f"""where intake.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_webhook(self):
        """Метод возвращает список id веб-хуков."""
        db_list_webhook = []
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(query=f"""select id from {ENV_OBJECT.db_connections()}.webhook.webhook """
                                 f"""where webhook.user_id = '{ENV_OBJECT.user_id()}'""")
            for row in cursor:
                db_list_webhook.append(*row)
        finally:
            cursor.close()
        return db_list_webhook

    def delete_webhook(self):
        """Метод чистит таблицу 'webhook.webhook'."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query=f"""delete from {ENV_OBJECT.db_connections()}.webhook.webhook """
                                 f"""where webhook.user_id = '{ENV_OBJECT.user_id()}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_all_setting(self):
        """Метод чистит все таблицы."""
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
        self.delete_webhook()
