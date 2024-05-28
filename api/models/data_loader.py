# data_loader.py
from sqlalchemy.orm import Session
from table import Company, FinancialInfo
from api.db import SessionLocal
from api.api.request import get_data2, get_financial_data

def load_data_to_db():
    session = SessionLocal()
    try:
        for page_number in range(1, 10):  # 페이지 번호 범위 설정
            company_data = get_data2(page_number, 10, 'itmsNm')  # 예제에서는 10개의 행을 가져옴
            for company_item in company_data:
                company_name = company_item['name']
                crno = company_item['crno']
                
                # 회사 정보 저장 또는 업데이트
                company = session.query(Company).filter_by(name=company_name).first()
                if not company:
                    company = Company(name=company_name, crno=crno)
                    session.add(company)
                    session.commit()
                
                # 재무 정보 가져오기
                financial_data = get_financial_data(crno)
                for fin_info in financial_data:
                    year = fin_info['year']
                    enpSaleAmt = fin_info['enpSaleAmt']
                    enpBzopPft = fin_info['enpBzopPft']
                    iclsPalClcAmt = fin_info['iclsPalClcAmt']
                    enpCrtmNpf = fin_info['enpCrtmNpf']
                    enpTastAmt = fin_info['enpTastAmt']
                    enpTdbtAmt = fin_info['enpTdbtAmt']
                    enpTcptAmt = fin_info['enpTcptAmt']
                    enpCptlAmt = fin_info['enpCptlAmt']
                    fnclDebtRto = fin_info['fnclDebtRto']
                    
                    db_fin_info = FinancialInfo(
                        company_id=company.id,
                        crno=crno,
                        year=year,
                        enpSaleAmt=enpSaleAmt,
                        enpBzopPft=enpBzopPft,
                        iclsPalClcAmt=iclsPalClcAmt,
                        enpCrtmNpf=enpCrtmNpf,
                        enpTastAmt=enpTastAmt,
                        enpTdbtAmt=enpTdbtAmt,
                        enpTcptAmt=enpTcptAmt,
                        enpCptlAmt=enpCptlAmt,
                        fnclDebtRto=fnclDebtRto
                    )
                    session.add(db_fin_info)
            session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    load_data_to_db()
