import numpy as np
import pandas as pd


# 라운드2의 모델5개의 예측값, 실제발전량으로 모델5개 중 가장 오차가 적은 예측값 가져오기
df_pred =  pd.read_csv("C:\Team3\Data\OIBC2023_data\pred.csv") # 모델5개의 예측값
df_gen = pd.read_csv("C:\Team3\Data\OIBC2023_data\gens.csv")    # 실제 발전량
pivoted_df = df_pred.pivot(index=['round', 'time'], columns='model_id', values='amount').reset_index()

# 열 이름 변경
pivoted_df.columns.name = None
pivoted_df.columns = ['round', 'time', 'model_1', 'model_2', 'model_3', 'model_4', 'model_5']

# round1의 모델별 예측량, 실제 발전량, 모델별 오차, 최적 모델
filtered_df_1 = pivoted_df[pivoted_df['round'] == 2]
filtered_df_1 = filtered_df_1.reset_index(drop=True)  # 행 인덱스를 0부터 시작하도록 재설정
filtered_df_1 = filtered_df_1.drop(columns=['round'])
filtered_df_1['gen'] = df_gen['amount']
# 빈 칸을 0으로 채우기
filtered_df_1 = filtered_df_1.fillna(0)


# 열 이름 목록 생성
model_columns = ['model_1', 'model_2', 'model_3', 'model_4', 'model_5']

# for 루프를 사용하여 열을 순회하며 오차 열 추가
for model_column in model_columns:
    error_column = 'error_rmse_' + model_column[-1]  # 열 이름 생성 (예: 'model_1' -> 'error_1')
    #rmse 구하기
    filtered_df_1[error_column] = np.sqrt((((filtered_df_1['gen'] - filtered_df_1[model_column]) / filtered_df_1['gen']) * 100)**2)

# 'error_rmse_1'에서 'error_rmse_5' 중에서 최솟값 찾기
filtered_df_1['optical'] = filtered_df_1[['error_rmse_1', 'error_rmse_2', 'error_rmse_3', 'error_rmse_4', 'error_rmse_5']].min(axis=1)

# 최솟값을 가지는 열 인덱스를 찾아 새로운 열 'optical_model'에 넣기
optical_model_columns = (filtered_df_1[['error_rmse_1', 'error_rmse_2', 'error_rmse_3', 'error_rmse_4', 'error_rmse_5']]
                         .idxmin(axis=1)
                         .apply(lambda x: model_columns[int(x[-1]) - 1] if not pd.isna(x) else 'None'))
filtered_df_1['optical_model'] = optical_model_columns

# 빈 칸을 0으로 채우기
filtered_df_1 = filtered_df_1.fillna(0)

# 모델 번호를 추출하여 새로운 열 'model_number'에 추가
filtered_df_1['model_number'] = filtered_df_1['optical_model'].str.extract(r'(\d+)')


filtered_df_1['optical_gen'] = 0  # 초기값으로 0 설정

for i in range(1, 6):
    mask = (filtered_df_1['model_number'] == str(i))
    filtered_df_1.loc[mask, 'optical_gen'] = filtered_df_1.loc[mask, 'model_' + str(i)]

# 0이 아닌 값이 있는 경우에만 0으로 설정
filtered_df_1['optical_gen'] = np.where(filtered_df_1['optical_gen'] != 0, filtered_df_1['optical_gen'], 0)


pred_round = pd.DataFrame({'time': filtered_df_1['time'], 'amount': filtered_df_1['optical_gen']})


# 빈 칸을 0으로 채우기
filtered_df_1 = filtered_df_1.fillna(0)


filtered_df_1.to_csv("C:\Team3\Data\OIBC2023_data\gen_pred_round2.csv", mode='w', index=False)
pred_round.to_csv("C:\Team3\Data\OIBC2023_data\optical_gen_round2.csv", mode='w', index=False)








