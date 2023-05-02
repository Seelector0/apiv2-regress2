"""Метод автоматической чистки всех БД"""


def test_clear_all_database(customer_api, connections, tracking_api):
    for i in connections.get_shops_list():
        customer_api.delete_connection(shop_id=i.shop_id)
    for i in connections.get_orders_list():
        tracking_api.delete_orders_list_in_tracking(order_id=i.order_id)
    connections.delete_all_setting()
