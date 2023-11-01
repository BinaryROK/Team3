
import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('weather_forecast.csv')

# round가 1일 때와 2일 때의 데이터 추출
df_round_1 = df[df['round'] == 1]
df_round_2 = df[df['round'] == 2]

# time을 기준으로 두 라운드의 데이터를 합치고 평균 계산
df_combined = pd.concat([df_round_1, df_round_2]).groupby('time').mean().reset_index()

# 결과를 CSV 파일로 저장
df_combined.to_csv('weather_forecast_mean.csv', index=False)

# pred.csv 파일 불러오기
data = pd.read_csv('pred.csv')

# 데이터 불러오기
df = pd.read_csv('pred.csv')

# 시간별 최대, 최소 값 계산
grouped = df.groupby('time')['amount'].apply(lambda x: x.nlargest(len(x)-2).nsmallest(len(x)-4).mean())

# 결과를 새로운 csv 파일로 저장
grouped.to_csv('pred_mean.csv', header=True)