import os
import pandas as pd


# 과거기상예보도 pred와 동일한 시간으로 맞추기


# 1. round 분리하기
# CSV 파일을 불러오기
df = pd.read_csv('C:\Team3\Data\LSTM_binary\weather_forecast.csv')

# 'round' 열의 고유 값 확인
unique_rounds = df['round'].unique()

file_dir = (r"C:\Team3\Data\LSTM_binary\processed\4_fcst_processed")
# 각 'round' 값에 대해 데이터를 분리하고 별도의 CSV 파일로 저장
for round_value in unique_rounds:
    # 'round' 값에 따라 데이터 필터링
    filtered_data = df[df['round'] == round_value]

    # CSV 파일 이름 설정
    file_name = f'round_{round_value}.csv'
    file_dir = (r"C:\Team3\Data\LSTM_binary\processed\4_fcst_processed")
    file_path = os.path.join(file_dir,file_name)
    filtered_data.to_csv(file_path, mode = 'w' ,index=False)

round1_df = pd.read_csv(os.path.join(file_dir, 'round_1.csv'))
round2_df = pd.read_csv(os.path.join(file_dir, 'round_2.csv'))



# 2. time 열의 값 일치하게 만들기

# time 열을 datetime 형식으로 변환합니다
round1_df['time'] = pd.to_datetime(round1_df['time'])
round2_df['time'] = pd.to_datetime(round2_df['time'])

# 두 데이터프레임에서 중복되는 시간 데이터를 선택합니다
common_times = set(round1_df['time']).intersection(set(round2_df['time']))

# 두 데이터프레임에서 공통된 시간 데이터만을 선택합니다
round1_df = round1_df[round1_df['time'].isin(common_times)]
round2_df = round2_df[round2_df['time'].isin(common_times)]

# 두 데이터프레임을 시간순으로 정렬합니다
round1_df = round1_df.sort_values(by='time')
round2_df = round2_df.sort_values(by='time')

fcst_file_name_1 = "round1_fcst_leak_deleted.csv"
fcst_file_name_2 = "round2_fcst_leak_deleted.csv"

file_path_1 = os.path.join(file_dir, fcst_file_name_1)
file_path_2 = os.path.join(file_dir, fcst_file_name_2)

round1_df.to_csv(file_path_1, mode='w', index=False)
round2_df.to_csv(file_path_2, mode='w', index=False)

