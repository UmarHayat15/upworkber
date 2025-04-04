from pricing_service.service import BaseService
from pricing_service.model.db import MarketMetadataDao


class MarketMetadataService(BaseService):
    def __init__(self):
        super().__init__(MarketMetadataDao)


