# algorithm.py
from sqlalchemy.orm import Session
from tables import Company, FinancialInfo
from api.db import SessionLocal

def perform_algorithm(company_name: str):
    session = SessionLocal()
    try:
        # company_name 기준으로 회사 검색
        company = session.query(Company).filter(Company.name == company_name).first()
        if not company:
            print(f"Company with name {company_name} not found")
            return
        
        # crno 기준으로 재무 정보 검색
        financial_infos = session.query(FinancialInfo).filter(FinancialInfo.crno == company.crno).all()

        # 특정 알고리즘을 수행하는 코드 (예: 평균 수익 계산)
        total_revenue = sum(fin_info.enpSaleAmt for fin_info in financial_infos)
        total_profit = sum(fin_info.enpBzopPft for fin_info in financial_infos)
        avg_revenue = total_revenue / len(financial_infos) if financial_infos else 0
        avg_profit = total_profit / len(financial_infos) if financial_infos else 0

        print(f"Company: {company.name}")
        print(f"Average Revenue: {avg_revenue}")
        print(f"Average Profit: {avg_profit}")

    finally:
        session.close()

if __name__ == "__main__":
    perform_algorithm("Some Company Name")
