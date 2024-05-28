from pydantic import BaseModel,Field

#DB 모음집

class TaskBase(BaseModel):
    title : str | None = Field(None, example="안녕하세요")

class TaskCreate(TaskBase):
    pass
    #crno
    #주가
    #등등
    #사실 다 나누는게 좋을것같지만 그건 귀찮으니 그냥 대충 하자


class TaskCreateResponse(TaskCreate):
    id: int
    class Config:
        orm_mode = True

class Task(TaskBase):#여기서 title만 가져가는건 그 데이터는 저장되어있다는 뜻
    id:int
    class Config:
        orm_mode=True


