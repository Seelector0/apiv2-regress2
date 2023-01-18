from sys import maxsize


class Warehouse:

    def __init__(self, name_warehouse=None, address_warehouse=None, warehouse_id=None, contact_person=None,
                 phone_contact_person=None, email_contact_person=None, regular_pickup_number_dpd=None):
        self.name_warehouse = name_warehouse
        self.address_warehouse = address_warehouse
        self.warehouse_id = warehouse_id
        self.contact_person = contact_person
        self.phone_contact_person = phone_contact_person
        self.email_contact_person = email_contact_person
        self.regular_pickup_number_dpd = regular_pickup_number_dpd

    def __repr__(self):
        return f"{self.warehouse_id}:{self.name_warehouse}"

    def __eq__(self, other):
        return (self.warehouse_id is None or other.warehouse_id is None or self.warehouse_id == other.warehouse_id) \
               and self.name_warehouse == other.name_warehouse

    def name_warehouse_max(self):
        if self.name_warehouse:
            return int(self.name_warehouse)
        else:
            return maxsize
