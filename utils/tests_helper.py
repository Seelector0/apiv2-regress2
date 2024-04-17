from databases.connections import DataBaseConnections


class TestsHelper:

    def __init__(self, app):
        self.app = app
        self.db_connections = DataBaseConnections()

    def check_methods_shop(self):
        """Проверка всех методов Shop"""
        for _ in range(2):
            self.app.tests_shop.post_shop()
        self.app.tests_shop.get_shop()
        self.app.tests_shop.get_shop_by_id()
        self.app.tests_shop.put_shop()
        self.app.tests_shop.patch_shop()

    def check_methods_warehouse(self):
        """Проверка всех методов Warehouse"""
        for _ in range(10):
            self.app.tests_warehouse.post_warehouse()
        self.app.tests_warehouse.warehouse_by_id()
        self.app.tests_warehouse.put_warehouse()
        self.app.tests_warehouse.get_warehouses()
        self.app.tests_warehouse.patch_warehouse_visibility()
        self.app.tests_warehouse.patch_warehouse_comment()
        self.app.tests_warehouse.patch_warehouse_email()
        self.app.tests_warehouse.patch_warehouse_full_name()
        self.app.tests_warehouse.patch_warehouse_phone()
        self.app.tests_warehouse.patch_warehouse_pickup()
        self.app.tests_warehouse.patch_warehouse_dpd_pickup_num()
        self.app.tests_warehouse.patch_warehouse_working_time()
        self.app.tests_warehouse.patch_warehouse_l_post_warehouse_id()
        self.app.tests_warehouse.delete_warehouse()

    def check_methods_delivery_service(self):
        if len(self.db_connections.get_list_shops()) == 0:
            self.app.tests_shop.post_shop()

