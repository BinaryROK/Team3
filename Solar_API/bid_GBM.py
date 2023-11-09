import pandas as pd
import numpy as np
import requests
import json
import params as pa
import solar_api as api
from Model.Model_saved import gen_GBM as g
import os
from datetime import datetime


# api로 기상예측데이터를 가져 온 후 이를 저장된 모델에 학습시켜 예측발전량을 반환하고 이를 Post로 입찰한다.  GBM모델사용


def solar_bid_10(Date):
    # 예측기상데이터
    df = pd.DataFrame(api._get_weather_fcst_10(Date))

    filename = "WeatherData_" + Date +'.csv'

    DataPath = os.path.join(r"C:\Team3\Data\WeatherData\10", filename)
    df.to_csv()
    df.to_csv(DataPath, index=False)

    # 예측 발전량 데이터프레임
    result_df = g.gen(DataPath)
    
    # 예측발전량 리스트(값24개)
    result_list = result_df['Predicted'].tolist()

    print(result_list)

    # JSON으로 변환하여 POST 요청
    success = requests.post(f'https://research-api.solarkim.com/cmpt-2023/bids', data=json.dumps(result_list), headers={
        'Authorization': f'Bearer {pa.SOLAR_APIKEY}'
    }).json()
    print(success)
    return


def solar_bid_17(Date):
    # 예측기상데이터
    df = pd.DataFrame(api._get_weather_fcst_17(Date))

    filename = "WeatherData_" + Date+'.csv'

    DataPath = os.path.join(r"C:\Team3\Data\WeatherData\17", filename)
    df.to_csv()
    df.to_csv(DataPath, index=False)

    # 예측 발전량 데이터프레임
    result_df = g.gen(DataPath)

    # 예측발전량 리스트(값24개)
    result_list = result_df['Predicted'].tolist()

    print(result_list)

    # JSON으로 변환하여 POST 요청
    success = requests.post(f'https://research-api.solarkim.com/cmpt-2023/bids', data=json.dumps(result_list), headers={
        'Authorization': f'Bearer {pa.SOLAR_APIKEY}'
    }).json()
    print(success)
    return

Date = "2023-11-9"
solar_bid_17(Date)