from pricing_service.db import ModelBase, BaseDao
from sqlalchemy import create_engine, Column, Integer, String

# Define the KnownProducts table as an ORM model
class KnownProduct(ModelBase):
    __tablename__ = "known_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)

    def __repr__(self):
        return f"<KnownProduct(id={self.id}, name='{self.name}', brand='{self.brand}')>"


class KnownProductDao(BaseDao):
    def __init__(self, engine):
        super().__init__(engine, KnownProduct)
