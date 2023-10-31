from keras.models import load_model
import pandas as pd
import keras
import joblib
import torch
import os
from datetime import datetime

import pandas as pd
import joblib


def gen(DataPath):
    model_directory = "C:\\Team3\\Data\\ModelData"

    # ModelData 디렉토리 안의 모든 디렉토리 목록 가져오기
    subdirectories = [os.path.join(model_directory, d) for d in os.listdir(model_directory) if os.path.isdir(os.path.join(model_directory, d))]

    # 각 디렉토리의 수정 시간을 가져와서 최신 디렉토리 선택
    latest_directory = max(subdirectories, key=os.path.getctime)

    # 스케일러 로드
    scaler_x = joblib.load(os.path.join(latest_directory,"scaler_x.pkl"))
    scaler_y = joblib.load(os.path.join(latest_directory,"scaler_y.pkl"))

    # 모델 경로
    model_path = os.path.join(latest_directory, "gen_model.h5")

    # 모델 로드
    model = load_model(model_path)


    # 새로운 데이터를 읽어옴 (예: new_data.csv)
    #new_data = pd.read_csv('C:\Team3\Data\SolarAPIData\WeatherData.csv')
    new_data = pd.read_csv(DataPath)
    # 'time' 열을 datetime 형식으로 변환
    new_data['time'] = pd.to_datetime(new_data['time'])

    # 데이터 전처리 (스케일링)
    new_data_values = new_data.drop('time', axis=1).values
    new_data_scaled = scaler_x.transform(new_data_values)

    # LSTM 입력 형태로 변환
    new_data_reshaped = new_data_scaled.reshape((new_data_scaled.shape[0], 1, new_data_scaled.shape[1]))

    # 모델로 예측
    new_yhat = model.predict(new_data_reshaped)

    # 예측값을 원래 스케일로 변환
    new_yhat_original = scaler_y.inverse_transform(new_yhat)


    new_data['Predicted'] = new_yhat_original
    result_df = new_data[['time']].copy()  # 'time' 열 복사
    result_df['Predicted'] = new_yhat_original  # 'Predicted' 열 추가

    result_df["Predicted"] = result_df["Predicted"].apply(lambda x: 0 if x < 0 else x)



    # 현재 시간을 포함한 파일 이름 생성
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f'gen_predicted_{current_time}.csv'

    # 저장할 디렉토리 경로
    output_directory = "C:\\Team3\\Data\\Predicted"

    # 결과를 CSV 파일로 저장
    result_df.to_csv(os.path.join(output_directory, file_name), index=False)

    return result_df
