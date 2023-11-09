import pandas as pd
import numpy as np
from keras.models import load_model
import joblib
import os


# 저장된 모델 및 스케일러를 불러올 디렉토리 경로
load_directory = r"C:\Team3\Data\ModelData\2023-11-07_06-20-50"
model_directory = os.path.join(load_directory, 'model')
scaler_directory = os.path.join(load_directory, 'scaler')

# 모델 및 스케일러 추출
loaded_models = []
loaded_scalers = []

for i in range(10):
    # 모델 불러오기
    loaded_model = load_model(os.path.join(model_directory, f"model_{i}.h5"))
    loaded_models.append(loaded_model)

    # 스케일러 불러오기
    loaded_scaler = joblib.load(os.path.join(scaler_directory, f"scaler_{i}.joblib"))
    loaded_scalers.append(loaded_scaler)


# 새로운 데이터 불러오기 (샘플 데이터, 실제 데이터로 대체)
new_data = pd.read_csv(r"C:\Team3\Data\WeatherData\10\WeatherData_2023-11-6.csv")
new_data['time'] = pd.to_datetime(new_data['time'])

# 데이터 전처리 (스케일링)
new_data_values = new_data.drop(['time'], axis=1)

# 예측 수행
predictions = []

for i, loaded_model in enumerate(loaded_models):
    # new_data_values를 모델의 입력 형상에 맞게 재구성
    new_data_values_reshaped = new_data_values.values.reshape((new_data_values.shape[0], 1, new_data_values.shape[1]))

    prediction_scaled = loaded_model.predict(new_data_values_reshaped)
    prediction = loaded_scalers[i].inverse_transform(prediction_scaled)  # 스케일러를 통해 역 변환
    prediction = np.maximum(prediction, 0)  # 예측값이 음수일 경우 0으로 대체
    predictions.append(prediction)


# 예측 결과를 데이터프레임으로 저장
results_list = []

for i, prediction in enumerate(predictions):
    result = pd.DataFrame({'time': new_data['time'], f'predicted_value_{i + 1}': prediction.flatten()})
    results_list.append(result)

# 예측 결과 데이터프레임 합치기
results = results_list[0]
for result in results_list[1:]:
    results = pd.merge(results, result, on='time', how='inner')

# 예측 결과 저장
results.to_csv("path_to_predictions.csv", index=False)
