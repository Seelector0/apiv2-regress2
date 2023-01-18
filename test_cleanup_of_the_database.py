"""Метод автоматической чистки всех БД"""


def test_clear_all_database(customer_api, connections, tracking_api):
    shops = connections.get_shops_list()
    for i in shops:
        customer_api.delete_connection(shop_id=i.shop_id)
    orders = connections.get_orders_list()
    for i in orders:
        tracking_api.delete_orders_list_in_tracking(order_id=i.order_id)
    connections.delete_all_setting()
