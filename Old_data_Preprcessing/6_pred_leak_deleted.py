import os
import pandas as pd



# 3_leak_delete의  round1 round2를  fcst와 시간을 맞추기
round1_df = pd.read_csv(r"C:\Team3\Data\LSTM_binary\processed\3_leak_delete\round_1_model_splitted_leak_deleted.csv")
round2_df = pd.read_csv(r"C:\Team3\Data\LSTM_binary\processed\3_leak_delete\round_2_model_splitted_leak_deleted.csv")
compare = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\4_fcst_processed\round1_fcst_leak_deleted.csv')


# time 열을 datetime 형식으로 변환합니다
round1_df['time'] = pd.to_datetime(round1_df['time'])
round2_df['time'] = pd.to_datetime(round2_df['time'])
compare['time'] = pd.to_datetime(compare['time'])

# 1. round1
# 두 데이터프레임에서 중복되는 시간 데이터를 선택합니다 (gens, compare)
common_times_1 = set(round1_df['time']).intersection(set(compare['time']))

# 두 데이터프레임에서 공통된 시간 데이터만을 선택합니다
round1_df = round1_df[round1_df['time'].isin(common_times_1)]
compare = compare[compare['time'].isin(common_times_1)]


# 두 데이터프레임을 시간순으로 정렬합니다
round1_df = round1_df.sort_values(by='time')
compare = compare.sort_values(by='time')



# 2.round2
# 두 데이터프레임에서 중복되는 시간 데이터를 선택합니다 (actual, compare)
common_times_2 = set(round2_df['time']).intersection(set(compare['time']))

# 두 데이터프레임에서 공통된 시간 데이터만을 선택합니다
round2_df = round2_df[round2_df['time'].isin(common_times_2)]
compare = compare[compare['time'].isin(common_times_2)]


# 두 데이터프레임을 시간순으로 정렬합니다
round2_df = round2_df.sort_values(by='time')
compare = compare.sort_values(by='time')

# 저장
file_dir = (r"C:\Team3\Data\LSTM_binary\processed\6_pred_leak_deleted")

fcst_file_name_1 = "pred_round1.csv"
fcst_file_name_2 = "pred_round2.csv"

file_path_1 = os.path.join(file_dir, fcst_file_name_1)
file_path_2 = os.path.join(file_dir, fcst_file_name_2)

round1_df.to_csv(file_path_1, mode='w', index=False)
round2_df.to_csv(file_path_2, mode='w', index=False)
