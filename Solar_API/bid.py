import pandas as pd
import numpy as np
import requests
import json
import params as pa
import solar_api as api
from Model.Model_saved import gen as g
import os
from datetime import datetime


# api로 기상예측데이터를 가져 온 후 이를 저장된 모델에 학습시켜 예측발전량을 반환하고 이를 Post로 입찰한다.

Date = "2023-11-5"





# 예측발전량 리스트만들기
df =  pd.DataFrame(api._get_weather_fcst_17(Date))

filename = "WeatherData_"+ Date

DataPath = os.path.join("C:\Team3\Data\WeatherData", filename)
df.to_csv()
df.to_csv(DataPath, index=False)

result_df = g.gen(DataPath)


result_list = result_df['Predicted'].tolist()



print(result_list)


# 발전예측값 Post 하기(입찰하기)
success = requests.post(f'https://research-api.solarkim.com/cmpt-2023/bids', data=json.dumps(result_list), headers={
                            'Authorization': f'Bearer {pa.SOLAR_APIKEY}'
                        }).json()
print(success)