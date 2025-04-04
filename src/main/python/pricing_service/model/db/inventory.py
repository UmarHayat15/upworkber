from pricing_service.db import ModelBase, BaseDao
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON


# Define the KnownProducts table as an ORM model
class InventoryItem(ModelBase):
    __tablename__ = "inventory_item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    acquisition_id = Column(Integer, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    category = Column(String, nullable=False)
    list_price = Column(Float, nullable=False)
    est_shipping_cost = Column(Float, nullable=True)
    est_shipping_weight = Column(Float, nullable=True)
    est_shipping_len = Column(Integer, nullable=True)
    est_shipping_width = Column(Integer, nullable=True)
    est_shipping_height = Column(Integer, nullable=True)
    images = Column(JSON, nullable=False)
    storage_location = Column(String, nullable=False)

    def __repr__(self):
        return f"<KnownProduct(id={self.id}, name='{self.name}', brand='{self.brand}')>"


class KnownProductDao(BaseDao):
    def __init__(self, engine, model=KnownProduct):
        super().__init__(engine, model)
