import requests
import json

#API로 데이터 가져오기 => 기업기본정보
def get_data(page_number,int,str):
    base_url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
    params = {
        "pageNo": page_number,
        "numOfRows": int,
        "resultType": "json",
        "serviceKey": "XjAOulAs6VTDHZEFyeermCWZGMt05tyiPeVEpWTocYYwFyMCMEKDr4ktytwl3n3HvLasZJWkO%2FN4JA1pCBGb0A%3D%3D"
    }
    response = requests.get(base_url, params=params)
    contents = response.text
    json_ob = json.loads(contents)
    body=json_ob['response']['body']['items']['item']
    values =''.join(item[str] for item in body)
    return values

#API로 데이터 가져오기 => 기업재무정보
def get_data2(base_url:str,page_number:int,num:int,star: str):
   # base_url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
    url = f"{base_url}&pageNo={page_number}&numOfRows={num}&resultType=json&serviceKey=XjAOulAs6VTDHZEFyeermCWZGMt05tyiPeVEpWTocYYwFyMCMEKDr4ktytwl3n3HvLasZJWkO%2FN4JA1pCBGb0A%3D%3D"
    response = requests.get(url)
    contents = response.text
    json_ob = json.loads(contents)
    body=json_ob['response']['body']['items']['item']
    values =''.join(item[star] for item in body)
    return values
