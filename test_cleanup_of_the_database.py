"""Метод автоматической чистки всех БД"""


def test_clear_all_database(customer_api, connections, tracking_api, widget_api):
    shop_ids = connections.get_list_shops()
    connections_ids = customer_api.get_connection_ids(shop_ids=shop_ids)
    widget_api.delete_widgets_id()
    customer_api.delete_configuration(connections_ids=connections_ids)
    for id_ in shop_ids:
        customer_api.delete_connection(shop_id=id_)
    for id_ in connections.get_list_orders():
        tracking_api.delete_list_orders_in_tracking(order_id=id_)
    connections.delete_all_setting()
