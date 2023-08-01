"""Метод автоматической чистки всех БД"""


def test_clear_all_database(customer_api, connections, tracking_api, widget_api):
    for id_ in connections.metaship.get_list_shops():
        customer_api.customer.delete_connection(shop_id=id_)
        widget_api.widget.delete_list_orders_in_tracking(shop_id=id_)
    for id_ in connections.metaship.get_list_orders():
        tracking_api.tracking.delete_list_orders_in_tracking(order_id=id_)
    connections.metaship.delete_all_setting()
