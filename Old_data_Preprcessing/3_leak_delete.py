import pandas as pd
import os


# 모델별로 정렬된 pred round1,2의 time열의 값을 일치하게 맞추기
# 두 데이터프레임을 읽어옵니다 (round1과 round2 데이터프레임이라고 가정합니다)
round1_df = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\2_model_split\round_1_model_splitted.csv')
round2_df = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\2_model_split\round_2_model_splitted.csv')

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


file_dir = (r"C:\Team3\Data\LSTM_binary\processed\3_leak_delete")
file_name_1 = "round_1_model_splitted_leak_deleted.csv"
file_name_2 = "round_2_model_splitted_leak_deleted.csv"

file_path_1 = os.path.join(file_dir, file_name_1)
file_path_2 = os.path.join(file_dir, file_name_2)

round1_df.to_csv(file_path_1, mode='w', index=False)
round2_df.to_csv(file_path_2, mode='w', index=False)
