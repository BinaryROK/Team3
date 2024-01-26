import requests
import json

import requests
import json
import params as pa
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz

_API_URL = "https://research-api.solarkim.com"
_API_KEY = pa.SOLAR_APIKEY
_AUTH_PARAM = {"headers": {"Authorization": f"Bearer {_API_KEY}"}}

def _get(url: str):
    """
    주어진 url의 리소스를 조회한다.

    Args:
        url (str): API url
    """
    response = requests.get(url, **_AUTH_PARAM)
    return response.json()



date = '2023-10-23'
bid_round = 1
# 예측발전량 조회
gen_fcst = requests.get(f'https://research-api.solarkim.com/cmpt-2023/gen-forecasts/{date}/{bid_round}', headers={
                            'Authorization': f'Bearer {pa.SOLAR_APIKEY}'
                        }).json()
print("예측발전량")
print(gen_fcst)


# 예측결과 조회
bid_results = requests.get(f'https://research-api.solarkim.com/open-proc/cmpt-2023/bid-results/{date}', headers={
                            'Authorization': f'Bearer {pa.SOLAR_APIKEY}'}).json()
print("예측결과")
print(bid_results)

