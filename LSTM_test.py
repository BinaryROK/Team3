import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# 데이터 읽어오기
test_x = pd.read_csv('weather_actual.csv')
test_y = pd.read_csv('pred0re.csv')

train_x = pd.read_csv('weather_forecast.csv')
train_y = pd.read_csv('pred0.csv')



# 'time' 열을 datetime 형식으로 변환
test_x['time'] = pd.to_datetime(test_x['time'])
test_y['time'] = pd.to_datetime(test_y['time'])
train_x['time'] = pd.to_datetime(train_x['time'])
train_y['time'] = pd.to_datetime(train_y['time'])

# 데이터 전처리
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

train_x_values = train_x.drop('time', axis=1).values
train_x_scaled = scaler_x.fit_transform(train_x_values)

train_y_values = train_y.drop('time', axis=1).values
train_y_scaled = scaler_y.fit_transform(train_y_values)

test_x_values = test_x.drop('time', axis=1).values
test_x_scaled = scaler_x.transform(test_x_values)

test_y_values = test_y.drop('time', axis=1).values
test_y_scaled = scaler_y.transform(test_y_values)

train_x_reshaped = train_x_scaled.reshape((train_x_scaled.shape[0], 1, train_x_scaled.shape[1]))
test_x_reshaped = test_x_scaled.reshape((test_x_scaled.shape[0], 1, test_x_scaled.shape[1]))

input_shape = (1, train_x_scaled.shape[1])

# LSTM 모델 생성
model = Sequential()
model.add(LSTM(50, input_shape=input_shape))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')


# 모델 훈련
history = model.fit(train_x_reshaped, train_y_scaled, epochs=10, batch_size=32, validation_data=(test_x_reshaped, test_y_scaled), verbose=2, shuffle=False)

# 예측
yhat = model.predict(test_x_reshaped)

# 예측값을 원래 스케일로 변환
yhat_original = scaler_y.inverse_transform(yhat)


# 'pred_re.csv' 파일에 예측값 열 추가
test_y['Predicted'] = yhat_original

# 결과를 파일로 저장
test_y.to_csv('pred_re.csv', index=False)



# 시각화
plt.figure(figsize=(15,6))
plt.plot(test_y_values, label='Actual')
plt.plot(yhat_original, label='Predicted')
plt.legend()
plt.show()
