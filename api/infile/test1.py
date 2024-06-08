from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
router = APIRouter()

import api.cruds.task as task_crud
from api.db import get_db
import api.schemas.task as task_schema
from api.api.request import get_data

# 기본적으로 hello 메시지를 반환
# POST : 외부 API로부터 데이터를 가져와 DB에 저장
# GET : 완료된 작업 목록을 DB에서 조회하여 반환 
@router.get("/")
def hello():
    return{"message":"hello"}
# /task 엔드포인터에 POST 요청을 처리함
# response_model은 task_schema.TaskCreateResponse의 목록임
# get_db 함수로 사용하여 DB 세션을 주입받음
# 페이지 번호를 1부터 9까지 반복하면서 get_data 호출하여 데이터를 가져옴
# 생성된 모든 작업을 리스트로 반환 
@router.post("/tasks", response_model=List[task_schema.TaskCreateResponse])
async def create_task(db: Session = Depends(get_db)):
    created_tasks = []
    for p in range(5,10):
        url2='http://apis.data.go.kr/1160100/service/GetFinaStatInfoService_V2/getSummFinaStat_V2'
        #data = get_data('http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo',p,1,'itmsNm')
        data2 = get_data(url2,p,1,'crno')
        data = get_data('http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService_V2/getCorpOutline_V2?crno={data2}',p,1,'corpNm')
        data3 = get_data(url2,p,1,'bizYear') # 사업연도
        data4 = get_data(url2,p,1,'enpSaleAmt') #기업매출금액
        data5 = get_data(url2,p,1,'enpBzopPft') #기업영업이익
        data6 = get_data(url2,p,1,'iclsPalClcAmt') # 포괄손익계산금액
        data7 = get_data(url2,p,1,'enpCrtmNpf') # 기업당기순이익
        data8 = get_data(url2,p,1,'enpTastAmt') # 기업총자산금액
        data9 = get_data(url2,p,1,'enpTdbtAmt') # 기업총부채금액
        data10 = get_data(url2,p,1,'enpTcptAmt') # 기업총자본금액
        data11 = get_data(url2,p,1,'enpCptlAmt') # 기업자본 금액
        data12 = get_data(url2,p,1,'fnclDebtRto') # 재무제포부채비율
        task_body = task_schema.TaskCreate(
            title=data,
            crno=data2,
            year=data3,
            enpSaleAmt=data4,
            enpBzopPft=data5,
            iclsPalClcAmt=data6,
            enpCrtmNpf=data7,
            enpTastAmt=data8,
            enpTdbtAmt=data9,
            enpTcptAmt=data10,
            enpCptlAmt=data11,
            fnclDebtRto=data12
        )
        created_task = task_crud.create_task(db, task_body)
        created_tasks.append(created_task)
    return created_tasks
