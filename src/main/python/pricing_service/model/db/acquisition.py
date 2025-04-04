from datetime import datetime
from pricing_service.db import ModelBase, BaseDao
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime


class Acquisition(ModelBase):
    __tablename__ = 'acquisition'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # title of the listing
    title = Column(String(255), nullable=False)
    # listing description
    description = Column(Text, nullable=True)
    local_listing_id = Column(Integer, nullable=False)
    amt_paid = Column(Float)
    date_acquired = Column(DateTime, default=datetime.utcnow)


class AcquisitionDao(BaseDao):
    def __init__(self, engine, model=Acquisition):
        super().__init__(engine, model)
