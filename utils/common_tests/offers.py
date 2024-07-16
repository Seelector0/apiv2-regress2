from utils.checking import Checking


class CommonOffers:

    @staticmethod
    def test_offers_common(app, shop_id, warehouse_id, delivery_service_code, expected_value=None, **kwargs):
        """Получение оферов"""
        offers = app.offers.get_offers(shop_id=shop_id, warehouse_id=warehouse_id,
                                       delivery_service_code=delivery_service_code, **kwargs)
        Checking.check_status_code(response=offers, expected_status_code=200)
        if expected_value is not None:
            Checking.checking_json_key(response=offers, expected_value=expected_value)
        if 'format_' in kwargs:
            Checking.check_delivery_services_in_widget_offers(response=offers, delivery_service=delivery_service_code)

