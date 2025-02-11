from utils.schemas.intake_schemas import IntakeSchema
from utils.schemas.offer_schemas import OfferSchema
from utils.schemas.order_schemas import OrderSchema
from utils.schemas.parcel_schemas import ParcelSchema


class SchemaInfo:
    offer = OfferSchema()
    order = OrderSchema()
    intake = IntakeSchema()
    parcel = ParcelSchema()


SCHEMAS = SchemaInfo()
