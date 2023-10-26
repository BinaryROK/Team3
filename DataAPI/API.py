import requests
import json
import requests

import requests

endpoint = "https://api.odcloud.kr/api/15043275/v1/uddi:96ea0361-3cd2-4590-b232-a5221e145f73?"
serviceKey = "serviceKey=l2Q9dvUn2KbVPRpoKz2%2FFXQEO26AxG0SGfSDnLCLoqpDwWMMFCAictbUgYXKOMlGGz8jPaOsjQ6ATpXFJiIOaQ%3D%3D&"
pagenumber = 1
numOfRows = 100
URL = endpoint + serviceKey + "pageNo=" + str(pagenumber) + "&numOfRows=" + str(numOfRows) + "&type=json"
# 요청 헤더 설정
headers = {
    "Authorization": URL  # "Authorization" 헤더에 API 키 값을 설정
}

# API에 GET 요청 보내기
response = requests.get(URL, headers=headers)

# 응답 확인
if response.status_code == 200:
    data = response.json()  # JSON 응답을 파싱
    # 데이터 처리

    print(data)
else:
    print(f"API 요청 실패: {response.status_code} - {response.text}")
