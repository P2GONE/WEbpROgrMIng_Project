from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


from api.db import Base


class Task(Base):
    __tablename__="stock"

    id=Column(Integer, primary_key=True)
    title = Column(String(1024))
    crno = Column(String(1024))
    year = Column(Integer)
    enpSaleAmt = Column(Float)
    enpBzopPft = Column(Float)
    iclsPalClcAmt = Column(Float)
    enpCrtmNpf = Column(Float)
    enpTastAmt = Column(Float)
    enpTdbtAmt = Column(Float)
    enpTcptAmt = Column(Float)
    enpCptlAmt = Column(Float)
    fnclDebtRto = Column(Float)