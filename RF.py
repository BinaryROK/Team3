import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

# 데이터 읽어오기
test_x = pd.read_csv('weather_actual.csv')
test_y = pd.read_csv('pred0re.csv')
train_x = pd.read_csv('weather_forecast_mean.csv')
train_y = pd.read_csv('pred_mean.csv')

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
best_model = RandomForestRegressor(n_estimators=100, max_depth=15, min_samples_split=2, min_samples_leaf=1, random_state=42)
best_model.fit(train_x_values_scaled, train_y_values_scaled.ravel())
#Best parameters: {'max_depth': 15, 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 100}

# 예측 수행
yhat_scaled = best_model.predict(test_x_values_scaled)

# 예측값을 역변환하여 저장
yhat = scaler_y.inverse_transform(yhat_scaled.reshape(-1, 1))
test_y['Predicted'] = yhat

# 결과 저장
test_y.to_csv('pred_re.csv', index=False)

# 결과 시각화
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 6))
plt.plot(yhat, label='Predicted', alpha=0.5)
plt.plot(train_y_values, label='Actual', alpha=0.7)
plt.legend()
plt.show()
