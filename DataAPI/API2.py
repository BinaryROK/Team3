import requests
import json
import requests
import pprint

import requests

pp = pprint.PrettyPrinter(indent=4)
endpoint = "https://infuser.odcloud.kr/oas/docs?namespace=15025486/v1"
#api_key = "l2Q9dvUn2KbVPRpoKz2%2FFXQEO26AxG0SGfSDnLCLoqpDwWMMFCAictbUgYXKOMlGGz8jPaOsjQ6ATpXFJiIOaQ%3D%3D"
api_key = "l2Q9dvUn2KbVPRpoKz2/FXQEO26AxG0SGfSDnLCLoqpDwWMMFCAictbUgYXKOMlGGz8jPaOsjQ6ATpXFJiIOaQ=="
response = requests.get(endpoint, headers={"Authorization": f"Bearer {api_key}"})


# 응답 확인
if response.status_code == 200:
    api_data = response.json()  # JSON 응답을 파싱하여 딕셔너리로 변환

    print(pp.pprint(api_data))
    # 데이터 처리

else:
    print(f"API 요청 실패: {response.status_code} - {response.text}")