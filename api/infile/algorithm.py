from sqlalchemy.orm import Session
import api.cruds.task as task_crud  # assuming your CRUD functions are in this module

def calculate_roe(net_profit, equity):
    if equity > 0:  # 자본이 0보다 큰지 확인
        roe = (net_profit / equity) * 100
    else:
        roe = 0
    return roe

def calculate_roa(net_profit, total_assets):
    if total_assets > 0:  # 총자산이 0보다 큰지 확인
        roa = (net_profit / total_assets) * 100
    else:
        roa = 0
    return roa

def calculate_de_ratio(total_debt, total_equity):
    if total_equity > 0:  # 총자본이 0보다 큰지 확인
        de_ratio = total_debt / total_equity
    else:
        de_ratio = 0
    return de_ratio

def calculate_score(task):
    """
    주어진 기업의 재무 지표를 바탕으로 점수를 계산합니다.
    점수는 100점 만점으로 계산됩니다.
    """
    score = 0

    # 기준 설정 및 가중치
    roe_threshold = 15
    roa_threshold = 15
    de_ratio_threshold = 0.5

    roe_weight = 0.2
    roa_weight = 0.2
    de_ratio_weight = 0.1

    # ROE 계산
    roe = calculate_roe(task.enpCrtmNpf, task.enpTcptAmt)

    # ROA 계산
    roa = calculate_roa(task.enpCrtmNpf, task.enpTastAmt)

    # D/E 비율 계산
    de_ratio = calculate_de_ratio(task.enpTdbtAmt, task.enpTcptAmt)

    # ROE 점수
    roe_score = min(roe / roe_threshold, 1) * 100
    score += roe_score * roe_weight

    # ROA 점수
    roa_score = min(roa / roa_threshold, 1) * 100
    score += roa_score * roa_weight

    # D/E 비율 점수
    de_ratio_score = (1 - min(de_ratio / de_ratio_threshold, 1)) * 100
    score += de_ratio_score * de_ratio_weight

    return score

def kell(db: Session):
    """
    알고리즘으로 계산 후 결과 값을 반환해주는 함수.
    완료된 상태의 모든 작업을 가져와 네 번째 작업의 제목(회사 이름)을 반환합니다.
    """
    # 완료된 상태의 모든 작업 가져오기
    tasks = task_crud.get_tasks_with_done(db)
    
    # 네 번째 작업의 제목(회사 이름) 가져오기 (0-based index, 네 번째 요소는 인덱스 3에 있음)
    if len(tasks) >= 4:
        fourth_task_title = tasks[3][1]
        return fourth_task_title
    else:
        return None  # 작업이 4개 미만인 경우 None 반환
