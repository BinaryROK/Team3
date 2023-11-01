import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
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

train_x_values = train_x.drop('time', axis=1)
train_y_values = train_y.drop('time', axis=1)
test_x_values = test_x.drop('time', axis=1)
test_y_values = test_y.drop('time', axis=1)

# 직접 하이퍼파라미터를 설정하여 모델 학습
best_model = RandomForestRegressor(n_estimators=100, max_depth=10, min_samples_split=2, min_samples_leaf=1, random_state=42)
best_model.fit(train_x_values, train_y_values.values.ravel())

# 교차 검증을 통한 성능 평가
cv_scores = cross_val_score(best_model, train_x_values, train_y_values.values.ravel(), cv=5)
mean_cv_score = np.mean(cv_scores)
print(f"평균 교차 검증 점수: {mean_cv_score}")

# 최적의 모델을 사용하여 예측
yhat = best_model.predict(test_x_values)

# 'pred_re.csv' 파일에 예측값 열 추가
test_y['Predicted'] = yhat

# 결과를 파일로 저장
test_y.to_csv('pred_re.csv', index=False)



plt.figure(figsize=(15, 6))
plt.plot(yhat, label='Predicted', alpha=0.5) # 투명도를 0.5로 설정
plt.plot(train_y_values, label='Actual', alpha=0.7) # 투명도를 0.7로 설정
plt.legend()
plt.show()

