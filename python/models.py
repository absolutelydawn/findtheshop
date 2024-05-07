###
# 기능설명 : mysql model 설정
# 작성자명 : 송한나 
# 작성일자 : 2024.05.01
###
from sqlalchemy import Column, TEXT, INT, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQL TABLE - Item
class Item(Base):
    __tablename__ = 'item'

    id = Column(INT, primary_key=True, nullable=False)
    productId = Column(BigInteger, nullable=False)
    title = Column(TEXT, nullable=False)
    link = Column(TEXT, nullable=False)
    image = Column(TEXT, nullable=False)
    lprice = Column(INT, nullable=False)
    
# SQL TABLE - Lowlink
class Lowlink(Base):
    __tablename__ = 'lowlink'

    productId = Column(BigInteger, primary_key=True,nullable=False)
