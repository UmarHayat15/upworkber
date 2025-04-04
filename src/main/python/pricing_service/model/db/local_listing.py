from datetime import datetime
from pricing_service.db import ModelBase, BaseDao
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, JSON, Numeric


class LocalListing(ModelBase):
    __tablename__ = 'local_listing'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # facebook / craigslist / etc
    market_name = Column(String(255), nullable=False)
    # title of the listing
    title = Column(String(255), nullable=False)
    # listing description
    description = Column(Text)
    price = Column(Numeric(10, 2))
    thumbnail = Column(String)
    url = Column(String(255), nullable=False)
    loc_country = Column(String)
    loc_state = Column(String)
    loc_city = Column(String)
    loc_sub_area = Column(String)
    category = Column(String)
    sub_category = Column(String)
    item_type = Column(String)
    review_score = Column(Integer)
    images = Column(JSON)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<LocalListing(id={self.id}, title={self.title}, price={self.price}, location={self.location})>"


class LocalListingDao(BaseDao):
    def __init__(self, engine):
        super().__init__(engine, LocalListing)
