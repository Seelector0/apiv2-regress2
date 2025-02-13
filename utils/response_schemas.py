from utils.schemas.intake_schemas import IntakeSchema
from utils.schemas.offer_schemas import OfferSchema
from utils.schemas.order_schemas import OrderSchema
from utils.schemas.parcel_schemas import ParcelSchema
from utils.schemas.shop_schemas import ShopSchema
from utils.schemas.warehouses_schemas import WarehousesSchema


class SchemaInfo:
    shop = ShopSchema()
    offer = OfferSchema()
    order = OrderSchema()
    intake = IntakeSchema()
    parcel = ParcelSchema()
    warehouses = WarehousesSchema()


SCHEMAS = SchemaInfo()
