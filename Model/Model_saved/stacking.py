import pandas as pd
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 데이터 불러오기
actual_generation = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\7_input_data\test_y.csv')
prediction_model_1 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\7_input_data\train_y_1.csv')
prediction_model_2 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\7_input_data\train_y_2.csv')

# 필요한 열만 추출
actual_generation = actual_generation[['round', 'time', 'amount']]
prediction_model_1 = prediction_model_1[['round', 'time', 'model_1']]
prediction_model_2 = prediction_model_2[['round', 'model_2']]

# 데이터 합치기
merged_data = actual_generation.merge(prediction_model_1, on=['round', 'time'], how='left')
merged_data = merged_data.merge(prediction_model_2, on=['round', 'time'], how='left')

# NaN 값 0으로 채우기
merged_data.fillna(0, inplace=True)

# 필요한 열만 선택
stacking_data = merged_data[['model_1', 'model_2']]

# 훈련 및 테스트 데이터로 분할
X = stacking_data[['model_1', 'model_2']].values
y = merged_data['amount'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 스태킹 모델 정의
estimators = [
    ('lr', LinearRegression()),
    ('dt', DecisionTreeRegressor()),
    ('rf', RandomForestRegressor()),
    ('svr', SVR())
]

stacking_regressor = StackingRegressor(
    estimators=estimators,
    final_estimator=LinearRegression()
)

# 스태킹 모델 훈련
stacking_regressor.fit(X_train, y_train)

# 스태킹 모델 예측
y_pred = stacking_regressor.predict(X_test)

# 성능 측정
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error (MAE): {mae}')
