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
    for p in range(1, 10):
        data = get_data(p, 1, 'itmsNm')
        task_body = task_schema.TaskCreate(title=data)
        created_task = task_crud.create_task(db, task_body)
        created_tasks.append(created_task)
    return created_tasks

# /task 엔드포인트에 GET 요청을 처리함
# get_db 함수를 사용하여 DB를 주입
@router.get("/tasks",response_model=list[task_schema.Task])#TaskCreateResponse로 바꾸기
async def list_task(db:Session = Depends(get_db)):
    return task_crud.get_tasks_with_done(db)
