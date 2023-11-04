import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
import joblib
import os
from datetime import datetime

# 데이터 읽어오기
test_x = pd.read_csv('C:\Team3\Data\OIBC2023_data\weather_actual.csv') # test_x 실제기상데이터 11616
test_y = pd.read_csv('C:\Team3\Data\OIBC2023_data\gens.csv') # test_y 실제 발전량 11616

train_x = pd.read_csv('C:\Team3\Data\OIBC2023_data\weather_forecast.csv') # 예측기상 23912
train_y = pd.read_csv('C:\Team3\Data\OIBC2023_data\gen_weighted.csv') # 예측 발전량
# 'time' 열을 datetime 형식으로 변환
for df in [test_x, test_y, train_x, train_y]:
    df['time'] = pd.to_datetime(df['time'])

# 데이터 전처리
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

train_x_values = train_x.drop(['time', 'round'], axis=1)
train_x_scaled = scaler_x.fit_transform(train_x_values)

train_y_values = train_y.drop(['time', 'round'], axis=1)
train_y_scaled = scaler_y.fit_transform(train_y_values)

test_x_values = test_x.drop('time', axis=1)
test_x_scaled = scaler_x.transform(test_x_values)

test_y_values = test_y.drop('time', axis=1).values
test_y_scaled = scaler_y.transform(test_y_values)

#######################################################################################
train_x_reshaped = train_x_scaled.reshape((train_x_scaled.shape[0], 1, train_x_scaled.shape[1]))
test_x_reshaped = test_x_scaled.reshape((test_x_scaled.shape[0], 1, test_x_scaled.shape[1]))

input_shape = (1, train_x_scaled.shape[1])

#######################################################################################
# GBM을 위한 그리드 서치 파라미터
gbm_param_grid = {
    'n_estimators': [50, 100, 200, 500, 1000],
    'learning_rate': [0.01, 0.03, 0.05, 0.1, 0.2],
    'max_depth': [2, 3, 4],
    'subsample': [0.8, 0.9, 1.0]
}

gbm = GradientBoostingRegressor()
# GBM 그리드 서치
gbm_search = GridSearchCV(gbm, gbm_param_grid, cv=10, n_jobs=-1, verbose=1, scoring='neg_mean_absolute_error')
gbm_search.fit(train_x_scaled, train_y_scaled.ravel())
best_gbm = gbm_search.best_estimator_

# 모델 학습 및 예측 (GBM)
yhat = best_gbm.predict(test_x_reshaped[:, 0, :]).reshape(-1, 1)
yhat = scaler_y.inverse_transform(yhat)
yhat = np.maximum(yhat, 0)  # 예측값이 음수일 경우 0으로 대체
#########################################################################


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



# 모델을 저장할 디렉토리 경로
model_directory = "C:\\Team3\\Data\\ModelData"

# 현재 시간을 기반으로 디렉토리 생성
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
model_directory = os.path.join(model_directory, current_time)

# 디렉토리 생성
os.makedirs(model_directory, exist_ok=True)

# 모델 파일 이름 생성
model_file_name = "best_gbm_model.pkl"

# 모델을 파일로 저장
joblib.dump(best_gbm, os.path.join(model_directory, model_file_name))


# 스케일러를 파일로 저장
scaler_x_file = os.path.join(model_directory, "scaler_x.pkl")
scaler_y_file = os.path.join(model_directory, "scaler_y.pkl")

joblib.dump(scaler_x, scaler_x_file)
joblib.dump(scaler_y, scaler_y_file)

#플롯 이미지 저장
plot_file_name = os.path.join(model_directory, "plot.png")

# 파일이 이미 존재하면 덮어쓰기 (기존 파일은 삭제)
plt.savefig(plot_file_name)

# 사용한 트레인 저장
train_x.to_csv(os.path.join(model_directory, "train_x.csv"), mode='w', index=False)
train_y.to_csv(os.path.join(model_directory, "train_y.csv"), mode='w', index=False)