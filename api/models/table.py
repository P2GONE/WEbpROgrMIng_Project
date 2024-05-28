from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

#stock이라는 이름의 테이블을 정의함 
from api.db import Base
import requests

class Task(Base):
    __tablename__="stock"

    id=Column(Integer, primary_key=True)
    title = Column(String(1024))

# companies라는 이름의 테이블 정의함 => 기업 테이블 기준
class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    crno = Column(String(255), unique=True, nullable=False)
# Company의 테이블에서 crno를 기준으로 Financial Info에서 검색하는 기능을 algorithm.py에 구현함

# 경제 정보를 저장함 => 기업 저장 정보 테이블
class FinancialInfo(Base):
    __tablename__ = 'financial_info'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    crno = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    enpSaleAmt = Column(Float, nullable=False)
    enpBzopPft = Column(Float, nullable=False)
    iclsPalClcAmt = Column(Float, nullable=False)
    enpCrtmNpf = Column(Float, nullable=False)
    enpTastAmt = Column(Float, nullable=False)
    enpTdbtAmt = Column(Float, nullable=False)
    enpTcptAmt = Column(Float, nullable=False)
    enpCptlAmt = Column(Float, nullable=False)
    fnclDebtRto = Column(Float, nullable=False)

    company = relationship('Company', back_populates='financial_info')

Company.financial_info = relationship('FinancialInfo', order_by=FinancialInfo.id, back_populates='company')
