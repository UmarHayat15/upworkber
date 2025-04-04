from datetime import datetime
from pricing_service.db import ModelBase, BaseDao
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, JSON, Numeric


class MarketMetadata(ModelBase):
    __tablename__ = 'market_metadata'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    market_name = Column(String(255), nullable=False)
    primary_location_id = Column(String(255), nullable=False)
    secondary_location_id = Column(String(255), nullable=True)
    category_id = Column(String(255), nullable=True)

    def __repr__(self):
        return (f"<MarketMetadata(id={self.id}, market_name='{self.market_name}', "
                f"primary_location_id='{self.primary_location_id}', "
                f"secondary_location_id='{self.secondary_location_id}', "
                f"category_id='{self.category_id}')>")


class MarketMetadataDao(BaseDao):
    def __init__(self, engine):
        super().__init__(engine, MarketMetadata)