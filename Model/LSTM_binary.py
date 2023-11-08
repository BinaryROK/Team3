import pandas as pd
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
import joblib
import os
from datetime import datetime



# 데이터 읽어오기

test_x = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\7_input_data\text_x.csv') # test_x 실제기상데이터 11577
test_y = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\7_input_data\test_y.csv') # test_y 실제 발전량 11577


train_x_1 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\7_input_data\train_x_1.csv') # 예측기상 round1 11577
train_x_2 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\7_input_data\train_x_2.csv') # 예측기상 round2 11577


train_y_1 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\7_input_data\train_y_1.csv') # 예측 발전량 round1 11592

train_y_1_1 = pd.DataFrame()
train_y_1_1['round'] = train_y_1['round']
train_y_1_1['time'] = train_y_1['time']
train_y_1_1['amount'] = train_y_1['model_1']

train_y_1_2 = pd.DataFrame()
train_y_1_2['round'] = train_y_1['round']
train_y_1_2['time'] = train_y_1['time']
train_y_1_2['amount'] = train_y_1['model_2']

train_y_1_3 = pd.DataFrame()
train_y_1_3['round'] = train_y_1['round']
train_y_1_3['time'] = train_y_1['time']
train_y_1_3['amount'] = train_y_1['model_3']

train_y_1_4 = pd.DataFrame()
train_y_1_4['round'] = train_y_1['round']
train_y_1_4['time'] = train_y_1['time']
train_y_1_4['amount'] = train_y_1['model_4']

train_y_1_5 = pd.DataFrame()
train_y_1_5['round'] = train_y_1['round']
train_y_1_5['time'] = train_y_1['time']
train_y_1_5['amount'] = train_y_1['model_5']


train_y_2 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\7_input_data\train_y_2.csv') # 예측 발전량 round1

train_y_2_1 = pd.DataFrame()
train_y_2_1['round'] = train_y_2['round']
train_y_2_1['time'] = train_y_1['time']
train_y_2_1['amount'] = train_y_2['model_1']

train_y_2_2 = pd.DataFrame()
train_y_2_2['round'] = train_y_2['round']
train_y_2_2['time'] = train_y_1['time']
train_y_2_2['amount'] = train_y_2['model_2']

train_y_2_3 = pd.DataFrame()
train_y_2_3['round'] = train_y_2['round']
train_y_2_3['time'] = train_y_1['time']
train_y_2_3['amount'] = train_y_2['model_3']

train_y_2_4 = pd.DataFrame()
train_y_2_4['round'] = train_y_2['round']
train_y_2_4['time'] = train_y_1['time']
train_y_2_4['amount'] = train_y_2['model_4']

train_y_2_5 = pd.DataFrame()
train_y_2_5['round'] = train_y_2['round']
train_y_2_5['time'] = train_y_1['time']
train_y_2_5['amount'] = train_y_2['model_5']



# 'time' 열을 datetime 형식으로 변환
for df in [train_x_1, train_x_2, train_y_1_1, train_y_1_2, train_y_1_3, train_y_1_4, train_y_1_5, train_y_2_1, train_y_2_2, train_y_2_3, train_y_2_4, train_y_2_5]:
    df['time'] = pd.to_datetime(df['time'])

# 데이터 전처리
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

train_x_values_1 = train_x_1.drop(['time', 'round'], axis=1)
train_x_values_2 = train_x_2.drop(['time', 'round'], axis=1)

train_x_scaled_1 = scaler_x.fit_transform(train_x_values_1)
train_x_scaled_2 = scaler_x.transform(train_x_values_2)

train_y_values_list = [train_y_1_1, train_y_1_2, train_y_1_3, train_y_1_4, train_y_1_5, train_y_2_1, train_y_2_2, train_y_2_3, train_y_2_4, train_y_2_5]
train_y_scaled_list = []

for train_y in train_y_values_list:
    train_y_values = train_y.drop(['time', 'round'], axis=1)
    train_y_scaled = scaler_y.fit_transform(train_y_values)
    train_y_scaled_list.append(train_y_scaled)

# LSTM 모델 정의
def create_lstm_model(input_shape, output_shape):
    inputs = Input(shape=(1, input_shape))
    lstm = LSTM(50)(inputs)
    outputs = Dense(output_shape)(lstm)
    model = Model(inputs=inputs, outputs=outputs)
    model.compile(loss='mse', optimizer='adam')
    return model

# 모델 생성
models = []

for i in range(len(train_y_scaled_list)):
    model = create_lstm_model(train_x_scaled_1.shape[1], train_y_scaled_list[i].shape[1])
    models.append(model)

# 모델 훈련
for i in range(len(models)):
    model = models[i]
    model.fit(train_x_scaled_1.reshape((train_x_scaled_1.shape[0], 1, train_x_scaled_1.shape[1])),
              train_y_scaled_list[i], epochs=10, batch_size=64, verbose=2, shuffle=False)

    # 추가로 train_x_2를 사용하여 모델 재훈련
    model.fit(train_x_scaled_2.reshape((train_x_scaled_2.shape[0], 1, train_x_scaled_2.shape[1])),
              train_y_scaled_list[i], epochs=10, batch_size=64, verbose=2, shuffle=False)



# 모델 및 스케일러 저장

# 저장할 디렉토리 경로
save_directory = "C:\Team3\Data\ModelData"

# 현재 시간을 기반으로 디렉토리 생성
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
save_directory = os.path.join(save_directory, current_time)

# 모델과 스케일러를 저장할 디렉토리 경로
model_directory = os.path.join(save_directory, 'model')
scaler_directory = os.path.join(save_directory, 'scaler')

# 디렉토리 생성
os.makedirs(model_directory)
os.makedirs(scaler_directory)



# 모델 저장 (스케일러 제외)
for i, model in enumerate(models):
    model.save(os.path.join(model_directory, f"model_{i}.h5"))

# 스케일러 저장 (스케일러_y도 여기에 저장)
for i, scaler in enumerate([scaler_x] + train_y_scaled_list):
    joblib.dump(scaler, os.path.join(scaler_directory, f"scaler_{i}.joblib"))
