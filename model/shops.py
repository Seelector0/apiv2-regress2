from sys import maxsize


class Shop:

    def __init__(self, shop_name=None, url_shop=None, shop_id=None, contact_person=None, phone=None):
        self.shop_name = shop_name
        self.url_shop = url_shop
        self.shop_id = shop_id
        self.contact_person = contact_person
        self.phone = phone

    def __repr__(self):
        return f"{self.shop_id}:{self.shop_name}"

    def __eq__(self, other):
        return (self.shop_id is None or other.shop_id is None or self.shop_id == other.shop_id) \
               and self.shop_name == other.shop_name

    def name_shop_max(self):
        if self.shop_name:
            return int(self.shop_name[3::])
        else:
            return maxsize
