import joblib
import os
import pandas as pd
import numpy as np

from Solar_API import solar_api as api
from Old_data_Preprcessing import _2_model_split as ms
import input as input

def gen_10(Date):
    # 모델 파일 이름과 디렉토리
    model_directory = r"C:\Team3\Data\ModelData\2023-11-08_22-24-38"
    model_file_name = "gbm_model.pkl"

    # 모델과 스케일러를 로드
    loaded_model = joblib.load(os.path.join(model_directory, model_file_name))
    # 스케일러 파일 경로 설정
    scaler_x_file = os.path.join(model_directory, "scaler_x.pkl")
    scaler_y_file = os.path.join(model_directory, "scaler_y.pkl")

    # 스케일러를 파일로부터 로드
    scaler_x = joblib.load(scaler_x_file)
    scaler_y = joblib.load(scaler_y_file)

    # 새로운 데이터를 불러온다 (new_data라 가정)
    new_data = input.input_10(Date)


    # 'time' 열을 datetime 형식으로 변환
    new_data['time'] = pd.to_datetime(new_data['time'])

    # 데이터 전처리 (new_data를 기존 데이터 전처리 방식과 동일하게 처리)
    new_data_values = new_data.drop('time', axis=1).values
    new_data_scaled = scaler_x.transform(new_data_values)

    new_data_reshaped = new_data_scaled.reshape((new_data_scaled.shape[0], 1, new_data_scaled.shape[1]))

    # 모델을 사용하여 새로운 데이터에 대한 예측 수행
    new_predictions = loaded_model.predict(new_data_scaled).reshape(-1, 1)

    new_predictions = scaler_y.inverse_transform(new_predictions)
    new_predictions = np.maximum(new_predictions, 0)


    new_data['Predicted'] = new_predictions
    result_df = new_data[['time']].copy()  # 'time' 열 복사
    result_df['Predicted'] = new_predictions  # 'Predicted' 열 추가

    result_df["Predicted"] = result_df["Predicted"].apply(lambda x: 0 if x < 0 else x)


    return result_df


def gen_17(Date):
    # 모델 파일 이름과 디렉토리
    model_directory = r"C:\Team3\Data\ModelData\2023-11-08_22-24-38"
    model_file_name = "gbm_model.pkl"

    # 모델과 스케일러를 로드
    loaded_model = joblib.load(os.path.join(model_directory, model_file_name))
    # 스케일러 파일 경로 설정
    scaler_x_file = os.path.join(model_directory, "scaler_x.pkl")
    scaler_y_file = os.path.join(model_directory, "scaler_y.pkl")

    # 스케일러를 파일로부터 로드
    scaler_x = joblib.load(scaler_x_file)
    scaler_y = joblib.load(scaler_y_file)

    # 새로운 데이터를 불러온다 (new_data라 가정)
    new_data = input.input_17(Date)


    # 'time' 열을 datetime 형식으로 변환
    new_data['time'] = pd.to_datetime(new_data['time'])

    # 데이터 전처리 (new_data를 기존 데이터 전처리 방식과 동일하게 처리)
    new_data_values = new_data.drop('time', axis=1).values
    new_data_scaled = scaler_x.transform(new_data_values)

    new_data_reshaped = new_data_scaled.reshape((new_data_scaled.shape[0], 1, new_data_scaled.shape[1]))

    # 모델을 사용하여 새로운 데이터에 대한 예측 수행
    new_predictions = loaded_model.predict(new_data_scaled).reshape(-1, 1)

    new_predictions = scaler_y.inverse_transform(new_predictions)
    new_predictions = np.maximum(new_predictions, 0)


    new_data['Predicted'] = new_predictions
    result_df = new_data[['time']].copy()  # 'time' 열 복사
    result_df['Predicted'] = new_predictions  # 'Predicted' 열 추가

    result_df["Predicted"] = result_df["Predicted"].apply(lambda x: 0 if x < 0 else x)


    return result_df

if __name__ == "__main__":
    Date = "2023-11-9"
    df = gen_10(Date)
    df1 = gen_17(Date)
    print(df)
    print(df1)
