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


def _post(url: str, data):
    """
    리소스 생성 데이터를 이용해서 주어진 url의 리소스를 생성한다.

    Args:
        url (str): API url
        data (dict): 리소스 생성용 데이터
    """
    response = requests.post(url, data=json.dumps(data), **_AUTH_PARAM)
    return response.json()

def _get_gen_forecasts_10(Date): # 10시 17시의 예측발전량 조회
    """
    더쉐어 예측 모델의 예측 발전량 조회, 입찰대상일의 5가지 예측 모델의 예측 발전량 값을 취득한다 (https://research-api.solarkim.com/docs#tag/Competition-2023/operation/get_gen_forecasts_date_cmpt_2023_gen_forecasts__date___bid_round__get 참고)
    """
    date = Date
    bid_round_17 = 2
    gen_fcst_17 = _get(f"{_API_URL}/cmpt-2023/gen-forecasts/{date}/{bid_round_17}")
    df_10 = pd.DataFrame(gen_fcst_17)


    # 'time' 열을 datetime 형식으로 변환
    df_10['time'] = pd.to_datetime(df_10['time'], utc=True)

    # 서울 시간대로 변환
    seoul_tz = pytz.timezone('Asia/Seoul')
    df_10['time'] = df_10['time'].dt.tz_convert(seoul_tz)

    return df_10


def _get_gen_forecasts_17(Date):  # 10시 17시의 예측발전량 조회
    """
    더쉐어 예측 모델의 예측 발전량 조회, 입찰대상일의 5가지 예측 모델의 예측 발전량 값을 취득한다 (https://research-api.solarkim.com/docs#tag/Competition-2023/operation/get_gen_forecasts_date_cmpt_2023_gen_forecasts__date___bid_round__get 참고)
    """
    date = Date
    bid_round_17 = 2
    gen_fcst_17 = _get(f"{_API_URL}/cmpt-2023/gen-forecasts/{date}/{bid_round_17}")
    df_17 = pd.DataFrame(gen_fcst_17)

    # 'time' 열을 datetime 형식으로 변환
    df_17['time'] = pd.to_datetime(df_17['time'], utc=True)

    # 서울 시간대로 변환
    seoul_tz = pytz.timezone('Asia/Seoul')
    df_17['time'] = df_17['time'].dt.tz_convert(seoul_tz)


    # 서울 시간대로 변환
    seoul_tz = pytz.timezone('Asia/Seoul')
    df_17['time'] = df_17['time'].dt.tz_convert(seoul_tz)

    return df_17


def _get_weathers_observeds(Date): # 기상관측데이터 24시간치 조회
    """
    기상데이터 일단위 기상관측데이터 조회, 당일에 대해 조회하면 현재시간 기준 24시간치 조회 (https://research-api.solarkim.com/docs#tag/Competition-2023/operation/get_weathers_observeds_date_cmpt_2023_weathers_observeds__date__get 참고)
    """
    date = Date
    weather_obsv = _get(f"{_API_URL}/cmpt-2023/weathers-observeds/{date}")
    df = pd.DataFrame(weather_obsv)

    # 'time' 열이 있는 경우에만 처리
    if 'time' in df.columns:
        # 'time' 열을 datetime 형식으로 변환
        df['time'] = pd.to_datetime(df['time'], utc=True)

        # 서울 시간대로 변환
        seoul_tz = pytz.timezone('Asia/Seoul')
        df['time'] = df['time'].dt.tz_convert(seoul_tz)

    # 'time' 열을 datetime 형식으로 변환
    #df['time'] = pd.to_datetime(df['time'], utc=True)

    # 서울 시간대로 변환
    #seoul_tz = pytz.timezone('Asia/Seoul')
    #df['time'] = df['time'].dt.tz_convert(seoul_tz)

    return df


def _get_bids_result(Date): # 더쉐어 예측모델의 발전량 예측 결과 조회
    """
    더쉐어 예측 모델의 예측 결과 조회 (https://research-api.solarkim.com/docs#tag/Competition-2023/operation/get_bids_result_date_cmpt_2023_bid_results__date__get 참고)
    """
    date = Date

    bid_results = _get(f"{_API_URL}/cmpt-2023/bid-results/{date}")
    print(bid_results)


def _post_bids():
    """
    일단위 태양광 발전량 입찰. 시간별 24개의 발전량을 입찰하며 API가 호출된 시간에 따라 입찰 대상일이 결정된다. (https://research-api.solarkim.com/docs#tag/Competition-2023/operation/post_bids_cmpt_2023_bids_post 참고)
    """
    amounts = [0.0] * 24
    success = _post(f"{_API_URL}/cmpt-2023/bids", amounts)
    print(success)


def Weather_DataFrame(start_date, end_date):
    current_date = start_date
    combined_df = pd.DataFrame()  # 빈 DataFrame을 생성

    while current_date <= end_date:
        current_date_str = current_date.strftime('%Y-%m-%d')  # datetime을 문자열로 변환

        weather_date_current = _get_weathers_observeds(current_date_str)

        combined_df = pd.concat([combined_df, weather_date_current], ignore_index=True)

        current_date += timedelta(days=1)  # 다음 날짜로 이동

    return combined_df

def Gen_DataFrame_10(start_date, end_date):
    current_date = start_date
    combined_df = pd.DataFrame()  # 빈 DataFrame을 생성
    while current_date <= end_date:
        current_date_str = current_date.strftime('%Y-%m-%d')  # datetime을 문자열로 변환

        gen_data = _get_gen_forecasts_10(current_date_str)

        combined_df = pd.concat([combined_df, gen_data], ignore_index=True)

        current_date += timedelta(days=1)  # 다음 날짜로 이동

    return combined_df

def Gen_DataFrame_17(start_date, end_date):
    current_date = start_date
    combined_df = pd.DataFrame()  # 빈 DataFrame을 생성
    while current_date <= end_date:
        current_date_str = current_date.strftime('%Y-%m-%d')  # datetime을 문자열로 변환

        gen_data = _get_gen_forecasts_17(current_date_str)

        combined_df = pd.concat([combined_df, gen_data], ignore_index=True)

        current_date += timedelta(days=1)  # 다음 날짜로 이동


    return combined_df



if __name__ == "__main__":
    start_date = datetime(2023, 10, 1)
    end_date = datetime(2023, 10, 31)
    Weather_DataFrame(start_date, end_date).to_csv(os.path.join(pa.SolarDataPath,'WeatherData.csv'), index=False)
    Gen_DataFrame_10(start_date, end_date).to_csv(os.path.join(pa.SolarDataPath,"GenData_10.csv"), index=False)
    Gen_DataFrame_17(start_date, end_date).to_csv(os.path.join(pa.SolarDataPath,"GenData_17.csv"), index=False)
    print(_get_weathers_observeds("2023-10-10"))


