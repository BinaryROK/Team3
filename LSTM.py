import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import GridSearchCV


train_x = pd.read_excel('trainx01.xlsx', index_col=0, parse_dates=True)
train_y = pd.read_excel('trainy01.xlsx', parse_dates=True)
test_x = pd.read_excel('testx01.xlsx', index_col=0, parse_dates=True)
test_y = pd.read_excel('testy01.xlsx', parse_dates=True)



scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

train_x_values = train_x.values
train_x_scaled = scaler_x.fit_transform(train_x_values)

train_y_values = train_y.values
train_y_scaled = scaler_y.fit_transform(train_y_values)

test_x_values = test_x.values
test_x_scaled = scaler_x.transform(test_x_values)

test_y_values = test_y.values
test_y_scaled = scaler_y.transform(test_y_values)


train_x_reshaped = train_x_scaled.reshape((train_x_scaled.shape[0], 1, train_x_scaled.shape[1]))
test_x_reshaped = test_x_scaled.reshape((test_x_scaled.shape[0], 1, test_x_scaled.shape[1]))


input_shape = (1, train_x_scaled.shape[1])

model = Sequential()
model.add(LSTM(50, input_shape=input_shape))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')


history = model.fit(train_x_reshaped, train_y_scaled, epochs=1000, batch_size=32, validation_data=(test_x_reshaped, test_y_scaled))

yhat = model.predict(test_x_reshaped)

yhat_original = scaler_y.inverse_transform(yhat)
test_y_original = scaler_y.inverse_transform(test_y_scaled)



# Linear Regression 학습 및 예측
lr = LinearRegression()
lr.fit(train_x_scaled, train_y_scaled)
yhat_lr = lr.predict(test_x_reshaped[:,0,:])
yhat_lr_original = scaler_y.inverse_transform(yhat_lr)
# GBM을 위한 그리드 서치 파라미터
gbm_param_grid = {
    'n_estimators': [50, 100, 200, 500, 1000],
    'learning_rate': [0.01, 0.03, 0.05, 0.1, 0.2],
    'max_depth': [2, 3, 4],
    'subsample': [0.8, 0.9, 1.0]
}

gbm = GradientBoostingRegressor()
rf = RandomForestRegressor()


# GBM 그리드 서치
gbm_search = GridSearchCV(gbm, gbm_param_grid, cv=5, n_jobs=-1, verbose=1, scoring='neg_mean_absolute_error')
gbm_search.fit(train_x_scaled, train_y_scaled.ravel())
best_gbm = gbm_search.best_estimator_

# Random Forest를 위한 그리드 서치 파라미터
rf_param_grid = {
    'n_estimators': [100, 200, 500, 1000],
    'max_depth': [None, 2, 3, 5],
    'min_samples_split': [2, 3, 5],
    'min_samples_leaf': [1, 2, 4]
}

# Random Forest 그리드 서치
rf_search = GridSearchCV(rf, rf_param_grid, cv=3, n_jobs=-1, verbose=1, scoring='neg_mean_absolute_error')
rf_search.fit(train_x_scaled, train_y_scaled.ravel())
best_rf = rf_search.best_estimator_

# 모델 학습 및 예측 (GBM)
yhat_gbm = best_gbm.predict(test_x_reshaped[:, 0, :]).reshape(-1, 1)
yhat_gbm_original = scaler_y.inverse_transform(yhat_gbm)

# 모델 학습 및 예측 (Random Forest)
yhat_rf = best_rf.predict(test_x_reshaped[:, 0, :]).reshape(-1, 1)
yhat_rf_original = scaler_y.inverse_transform(yhat_rf)




# 그래프 그리기
plt.figure(figsize=(15,6))
plt.plot(test_y_original, label='Actual')
plt.plot(yhat_original, label='LSTM Predicted')
plt.plot(yhat_lr_original, label='LR Predicted')
plt.plot(yhat_gbm_original, label='GBM Predicted')
plt.plot(yhat_rf_original, label='RF Predicted')
plt.legend()
plt.show()


def calculate_mae(actual, predicted):
    return np.mean(np.abs(actual - predicted))

# LSTM의 MAE 계산
mae_lstm = calculate_mae(test_y_original, yhat_original)

# Linear Regression의 MAE 계산
mae_lr = calculate_mae(test_y_original, yhat_lr_original)

# GBM의 MAE 계산
mae_gbm = calculate_mae(test_y_original, yhat_gbm_original)

# Random Forest의 MAE 계산
mae_rf = calculate_mae(test_y_original, yhat_rf_original)

print("LSTM MAE:", mae_lstm)
print("LR MAE:", mae_lr)
print("GBM MAE:", mae_gbm)
print("RF MAE:", mae_rf)
