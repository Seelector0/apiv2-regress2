

class DeliveryService:

    def __init__(self, delivery_service=None, ds_shop_name=None, russian_post_token=None, russian_post_key=None,
                 ops_delivery=None, ds_id=None):
        self.ds_shop_name = ds_shop_name
        self.delivery_service = delivery_service
        self.russian_post_token = russian_post_token
        self.russian_post_key = russian_post_key
        self.ops_delivery = ops_delivery
        self.ds_id = ds_id

    def __repr__(self):
        return f"{self.ds_shop_name}:{self.ds_id}"
