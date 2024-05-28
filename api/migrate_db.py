from sqlalchemy import create_engine
from api.models.table import Base

#DB_URL로 DB 연결 
DB_URL="mysql+pymysql://root@db:3306/demo?charset=utf8"
#create_engine 함수로 DB_URL을 바탕으로 DB 엔진 생성 
engine=create_engine(DB_URL,echo=True)

#DB reset, 모든 테이블 drop 후 다시 create 
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__=="__main__":
    reset_database()