# MySQL testdb의 ProductIDs table과 연결하기
# 작성자명 : 장다은
# 작성일자 : 240430
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProductID(Base):
    __tablename__ = 'ProductIDs'
    product_id = Column(String(255), primary_key=True, nullable=False)
    