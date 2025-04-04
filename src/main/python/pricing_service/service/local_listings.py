from pricing_service.service import BaseService
from pricing_service.model.db import LocalListingDao
from enum import IntEnum


class ListingState(IntEnum):

    REMOVED_SOLD = -11

    NOT_REVIEWED = -10

    NEW_LISTING = 0

    ### NEEDS REVIEW
    AWAITING_DETAIL = 1
    AWAITING_PRODUCT_ID = 2
    AWAITING_PRICING = 3
    AWAITING_SHIPPING_DETAILS = 4
    AWAITING_LISTING_SCORE = 5

    ### LETS GO!
    AWAITING_LEAD_GENERATION = 10


class LocalListingService(BaseService):
    def __init__(self):
        super().__init__(LocalListingDao)


