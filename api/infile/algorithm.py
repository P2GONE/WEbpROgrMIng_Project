from sqlalchemy.orm import Session
import api.cruds.task as task_crud  # assuming your CRUD functions are in this module

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

def score_tasks(db: Session):
    """
    DB에서 모든 완료된 작업을 가져와 각 작업의 점수를 계산합니다.
    """
    tasks = task_crud.get_tasks_with_done(db)
    scored_tasks = []
    for task in tasks:
        score = calculate_score(task)
        scored_tasks.append({
            "task": task,
            "score": score
        })
    return scored_tasks


def calculate_score(task):
    """
    주어진 기업의 재무 지표를 바탕으로 점수를 계산합니다.
    점수는 100점 만점으로 계산됩니다.
    """
    score = 0

    # 기준 설정 및 가중치
    de_ratio_threshold = 0.5
    roe_threshold = 15
    roa_threshold = 15
    net_profit_margin_threshold = 10
    operating_profit_margin_threshold = 15
    comprehensive_income_ratio_threshold = 15
    debt_ratio_threshold = 0.5

    de_ratio_weight = 0.1
    roe_weight = 0.2
    roa_weight = 0.2
    net_profit_margin_weight = 0.1
    operating_profit_margin_weight = 0.1
    comprehensive_income_ratio_weight = 0.1
    debt_ratio_weight = 0.2

    # D/E 비율 점수
    # 부채 비율이 낮을수록 점수가 높음. 부채비율이 기준 이하일 경우 100점, 기준 이상일 경우 최소 0점을 받음
    de_ratio_score = (1 - min(task.fnclDebtRto / de_ratio_threshold, 1)) * 100
    score += de_ratio_score * de_ratio_weight
    
    # ROE 점수
    # 자기자본수익률이 높을 수록 점수가 높음. 자기자본수익률이 기준 이상일 경우 100점을 받고, 기준 이하일 경우 해당 비율에 비례한 점수를 받음
    roe_score = min(task.roe / roe_threshold, 1) * 100
    score += roe_score * roe_weight

    # ROA 점수
    # 자산수익률이 기준 이상일 경우 100점을 받고, 기준 이하일 경우 해당 비율에 비례한 점수를 받음.
    roa_score = min(task.roa / roa_threshold, 1) * 100
    score += roa_score * roa_weight

    # 순이익률 점수
    # 순이익률이 높을수록 점수가 높아집니다.순이익률이 기준 이상일 경우 100점을 받고, 기준 이하일 경우 해당 비율에 비례한 점수를 받습니다.
    net_profit_margin_score = min(task.net_profit_margin / net_profit_margin_threshold, 1) * 100
    score += net_profit_margin_score * net_profit_margin_weight

    # 영업이익률 점수
    # 영업이익률이 높을수록 점수가 높아집니다. 영업이익률이 기준 이상일 경우 100점을 받고, 기준 이하일 경우 해당 비율에 비례한 점수를 받습니다.
    operating_profit_margin_score = min(task.operating_profit_margin / operating_profit_margin_threshold, 1) * 100
    score += operating_profit_margin_score * operating_profit_margin_weight

    # 포괄이익 비율 점수
    # 포괄이익 비율이 높을수록 점수가 높아집니다. 포괄이익 비율이 기준 이상일 경우 100점을 받고, 기준 이하일 경우 해당 비율에 비례한 점수를 받습니다.
    comprehensive_income_ratio_score = min(task.comprehensive_income_ratio / comprehensive_income_ratio_threshold, 1) * 100
    score += comprehensive_income_ratio_score * comprehensive_income_ratio_weight

    # 부채 비율 점수
    # 부채비율이 높을수록 점수가 낮아집니다. 부채비율이 기준 이하일 경우 100점을 받고, 기준 이상일 경우 최소 0점을 받도록 합니다.
    debt_ratio_score = (min(task.debt_ratio / debt_ratio_threshold, 1)) * 100
    score += debt_ratio_score * debt_ratio_weight

    return score
