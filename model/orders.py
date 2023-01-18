from sys import maxsize


class Order:

    def __init__(self, fio=None, phone_number=None, order_id=None, email=None, comment=None, name_items=None,
                 article=None, price=None, count=None, declared_value=None, item_weight=None, shop_number=None,
                 pay_on_delivery=None, ds_number=None, address=None, weight=None, length=None, width=None, height=None):
        self.shop_number = shop_number
        self.fio = fio
        self.phone_number = phone_number
        self.email = email
        self.comment = comment
        self.name_items = name_items
        self.article = article
        self.price = price
        self.count = count
        self.declared_value = declared_value
        self.item_weight = item_weight
        self.pay_on_delivery = pay_on_delivery
        self.order_id = order_id
        self.ds_number = ds_number
        self.address = address
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height

    def __repr__(self):
        return f"{self.order_id}:{self.shop_number}"

    def __eq__(self, other):
        return (self.order_id is None or other.order_id is None or self.order_id == other.order_id) and \
               self.shop_number == other.shop_number

    def shop_number_or_max(self):
        if self.shop_number:
            return int(self.shop_number)
        else:
            return maxsize
