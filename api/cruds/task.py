from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session

import api.models.table as task_model
import api.schemas.task as task_schema

# create_task 함수는 새로운 작업을 DB에 추가
# DB : DB 세션임
# task_model.Task 객체를 생성, 데이터베이스에서 최신 상태를 가져와 task 객체를 갱신 
def create_task(db: Session,task_create:task_schema.TaskCreate)->task_model.Task:
    task=task_model.Task(**task_create.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# get_tasks_with_done 함수는 완료된 작업 목록을 가져옴
# DB : DB세션임
# Task 테이블에서 id와 title 칼럼을 선택하는 쿼리를 생성함
# 리스트 형태로 반환
def get_tasks_with_done(db: Session)->list[tuple[int,str]]:
    result:Result = db.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Task.crno,
            task_model.Task.year, 
            task_model.Task.enpSaleAmt,
            task_model.Task.enpBzopPft,
            task_model.Task.iclsPalClcAmt,
            task_model.Task.enpCrtmNpf,
            task_model.Task.enpTastAmt,
            task_model.Task.enpTdbtAmt,
            task_model.Task.enpTcptAmt,
            task_model.Task.enpCptlAmt,
            task_model.Task.fnclDebtRto,
        )
    )
    
    return result.all()


