from keras.models import load_model
import pandas as pd
import keras
import joblib
import torch

import pandas as pd
import joblib

# 모델 로드
model = load_model("C:/Team3/Model/Model_saved/keras_model.h5")

# 스케일러 로드
scaler_x = joblib.load("C:/Team3/Model/Model_saved/scaler_x.pkl")
scaler_y = joblib.load("C:/Team3/Model/Model_saved/scaler_y.pkl")

# 새로운 데이터를 읽어옴 (예: new_data.csv)
new_data = pd.read_csv('C:/Team3/Data/SolarAPIData/WeatherData.csv')

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


# 예측 결과 출력
print("Predicted values:")
print(new_yhat_original)
print(new_data['time'])

new_data['Predicted'] = new_yhat_original
result_df = new_data[['time']].copy()  # 'time' 열 복사
result_df['Predicted'] = new_yhat_original  # 'Predicted' 열 추가
print(result_df)

result_df.to_csv('C:\Team3\Data\Predicted\predicted_new_data.csv', index=False)

# Display or save the resulting DataFrame
