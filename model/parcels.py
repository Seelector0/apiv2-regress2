from sys import maxsize


class Parcel:

    def __init__(self, parcel_id=None, rid=None, number_of_orders=None, data_parcel=None):
        self.parcel_id = parcel_id
        self.rid = rid
        self.number_of_orders = number_of_orders
        self.data_parcel = data_parcel

    def __repr__(self):
        return f"{self.parcel_id}:{self.rid}"

    def __eq__(self, other):
        return (self.parcel_id is None or other.parcel_id is None or self.parcel_id == other.parcel_id) \
               and self.rid == other.rid

    def rid_or_max(self):
        if self.rid:
            return int(self.rid)
        else:
            return maxsize


class OrdersInParcel:

    def __init__(self, shop_number=None, ds_number=None):
        self.shop_number = shop_number
        self.ds_number = ds_number

    def __repr__(self):
        return f"{self.ds_number}:{self.shop_number}"

    def __eq__(self, other):
        return (self.ds_number is None or other.ds_number is None or self.ds_number == other.ds_number) \
               and self.shop_number == other.shop_number

    def shop_number_max(self):
        if self.shop_number:
            return int(self.shop_number)
        else:
            return maxsize
