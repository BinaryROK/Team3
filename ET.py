import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import ExtraTreesRegressor
import matplotlib.pyplot as plt

# 데이터 읽어오기
test_x = pd.read_csv('weather_actual.csv')
test_y = pd.read_csv('gens.csv')

train_x = pd.read_csv('weather_forecast.csv')
train_y = pd.read_csv('optical_gen_merged.csv')

# 'time' 열을 datetime 형식으로 변환
test_x['time'] = pd.to_datetime(test_x['time'])
test_y['time'] = pd.to_datetime(test_y['time'])
train_x['time'] = pd.to_datetime(train_x['time'])
train_y['time'] = pd.to_datetime(train_y['time'])


# 데이터 전처리
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

train_x_values = train_x.drop('time', axis=1)
train_y_values = train_y.drop('time', axis=1)
test_x_values = test_x.drop('time', axis=1)

# 모델 학습을 위해 데이터 변환
scaler_x.fit(train_x_values)
scaler_y.fit(train_y_values)

train_x_values_scaled = scaler_x.transform(train_x_values)
train_y_values_scaled = scaler_y.transform(train_y_values)
test_x_values_scaled = scaler_x.transform(test_x_values)

# 모델 학습
best_model = ExtraTreesRegressor(n_estimators=200, max_depth=40, min_samples_split=2, min_samples_leaf=1, random_state=42)
best_model.fit(train_x_values_scaled, train_y_values_scaled.ravel())
#Best parameters:  {'n_estimators': 200, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_depth': 40}

# 예측 수행
yhat_scaled = best_model.predict(test_x_values_scaled)

# 예측값을 역변환하여 원래 스케일로 되돌리기
yhat = scaler_y.inverse_transform(yhat_scaled.reshape(-1, 1))

# 시각화를 위해 데이터프레임으로 변환
results = pd.DataFrame({'time': test_x['time'], 'predicted_value': yhat.flatten()})

# 실제값과 예측값 비교를 시각화
plt.figure(figsize=(12, 6))
plt.plot(test_y['time'], test_y['amount'], label='Actual')
plt.plot(results['time'], results['predicted_value'], label='Predicted', linestyle='dashed')
plt.xlabel('Time')
plt.ylabel('Amount')
plt.legend()
plt.show()