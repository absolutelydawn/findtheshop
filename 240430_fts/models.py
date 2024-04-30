from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProductID(Base):
    __tablename__ = 'ProductIDs'
    product_id = Column(String(255), primary_key=True, nullable=False)
    