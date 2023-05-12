from psycopg2.extras import DictCursor


class DataBaseConnections:

    def __init__(self, metaship):
        self.metaship = metaship

    def get_list_shops(self):
        """Функция собирает (возвращает) список магазинов из таблицы 'customer.shop'"""
        db_list_shops = []
        cursor = self.metaship.connection_open().cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(f"select id from {self.metaship.db_connections}.customer.shop "
                           f"""where shop.user_id = '{self.metaship.user_id}'""")
            for row in cursor:
                db_list_shops.append(*row)
        finally:
            cursor.close()
        return db_list_shops

    def delete_list_shops(self):
        """Функция чистит таблицу 'customer.shop'"""
        cursor = self.metaship.connection_open().cursor()
        try:
            cursor.execute(f"delete from {self.metaship.db_connections}.customer.shop "
                           f"where shop.user_id = '{self.metaship.user_id}'")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_warehouses(self):
        """Функция собирает (возвращает) список складов из таблицы 'customer.warehouse'"""
        db_list_warehouses = []
        cursor = self.metaship.connection_open().cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(f"select id from {self.metaship.db_connections}.customer.warehouse "
                           f"""where warehouse.user_id = '{self.metaship.user_id}'""")
            for row in cursor:
                db_list_warehouses.append(*row)
        finally:
            cursor.close()
        return db_list_warehouses

    def delete_list_warehouses(self):
        """Функция чистит таблицу 'customer.warehouse'"""
        cursor = self.metaship.connection_open().cursor()
        try:
            cursor.execute(f"delete from {self.metaship.db_connections}.customer.warehouse "
                           f"where warehouse.user_id = '{self.metaship.user_id}'")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_delivery_services(self):
        """Функция собирает (возвращает) список подключенных служб доставок из таблицы 'customer.credential'"""
        db_list_delivery_service = []
        cursor = self.metaship.connection_open().cursor()
        try:
            cursor.execute(f"select id from {self.metaship.db_connections}.customer.credential "
                           f"""where customer.shop.user_id = '{self.metaship.user_id}'""")
            for row in cursor:
                db_list_delivery_service.append(*row)
        finally:
            cursor.close()
        return db_list_delivery_service

    def delete_list_delivery_services(self):
        """Функция чисти таблицу 'customer.credential'"""
        cursor = self.metaship.connection_open().cursor()
        try:
            cursor.execute(f"delete from {self.metaship.db_connections}.customer.credential "
                           f"where credential.user_id = '{self.metaship.user_id}'")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_drafts(self):
        """Функция собирает (возвращает) список черновиков из таблицы 'order.draft'"""
        db_list_drafts = []
        cursor = self.metaship.connection_open().cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(f'select id from {self.metaship.db_connections}."order".draft '
                           f"""where draft.user_id = = '{self.metaship.user_id}'""")
            for row in cursor:
                db_list_drafts.append(*row)
        finally:
            cursor.close()
        return db_list_drafts

    def delete_list_drafts(self):
        """Функция чистит таблицу 'order.draft'"""
        cursor = self.metaship.connection_open().cursor()
        try:
            cursor.execute(f'delete from {self.metaship.db_connections}."order".draft '
                           f"""where draft.user_id = '{self.metaship.user_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_orders(self):
        """Функция собирает (возвращает) список заказов из таблицы 'order.order'"""
        db_list_order = []
        cursor = self.metaship.connection_open().cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(f'select id from {self.metaship.db_connections}."order"."order" '
                           f"""where "order".user_id = '{self.metaship.user_id}'""")
            for row in cursor:
                db_list_order.append(*row)
        finally:
            cursor.close()
        return db_list_order

    def delete_list_orders(self):
        """Функция чистит таблицу 'order.order'"""
        cursor = self.metaship.connection_open().cursor()
        try:
            cursor.execute(f'delete from {self.metaship.db_connections}."order"."order" '
                           f"""where "order".user_id = '{self.metaship.user_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def get_list_parcels(self):
        """Функция собирает (возвращает) список партий из таблицы 'order.parcel'"""
        db_list_parcel = []
        cursor = self.metaship.connection_open().cursor(cursor_factory=DictCursor)
        try:
            cursor.execute(f'select id from {self.metaship.db_connections}."order".parcel '
                           f"""where parcel.user_id = '{self.metaship.user_id}'""")
            for row in cursor:
                db_list_parcel.append(*row)
        finally:
            cursor.close()
        return db_list_parcel

    def delete_list_parcels(self):
        """Функция чистит таблицу 'order.parcel'"""
        cursor = self.metaship.connection_open().cursor()
        try:
            cursor.execute(f'delete from {self.metaship.db_connections}."order".parcel '
                           f"""where parcel.user_id = '{self.metaship.user_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_order_document(self, order_id):
        r"""Функция чистит таблицу 'order.order_document'.
        :param order_id: ID заказа в БД.
        """
        cursor = self.metaship.connection_open().cursor()
        try:
            cursor.execute(f'delete from {self.metaship.db_connections}."order".order_document '
                           f"""where order_document.order_id = '{order_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_order_parcel(self, parcel_id):
        r"""Функция чистит таблицу 'order.order_parcel'.
        :param parcel_id: ID партии в БД.
        """
        cursor = self.metaship.connection_open().cursor()
        try:
            cursor.execute(f'delete from {self.metaship.db_connections}."order".order_parcel '
                           f"""where order_parcel.parcel_id = '{parcel_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_order_path(self):
        """Функция чистит таблицу 'order.order_path'"""
        cursor = self.metaship.connection_open().cursor()
        try:
            cursor.execute(f'delete from {self.metaship.db_connections}."order".order_patch '
                           f"""where order_patch.user_id = '{self.metaship.user_id}'""")
            cursor.connection.commit()
        finally:
            cursor.close()

    def delete_all_setting(self):
        """Функция удаляет всё выше перечисленное"""
        self.delete_list_shops()
        self.delete_list_warehouses()
        self.delete_list_delivery_services()
        self.delete_list_drafts()
        for id_ in self.get_list_orders():
            self.delete_order_document(order_id=id_)
        self.delete_list_orders()
        for id_ in self.get_list_parcels():
            self.delete_order_parcel(parcel_id=id_)
        self.delete_order_path()
        self.delete_list_parcels()
