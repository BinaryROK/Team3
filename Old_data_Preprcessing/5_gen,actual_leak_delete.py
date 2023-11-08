import os
import pandas as pd


# gens와 actual_weather을 fcst와 시간을 맞추기
gens = pd.read_csv(r"C:\Team3\Data\LSTM_binary\gens.csv")
actual = pd.read_csv(r"C:\Team3\Data\LSTM_binary\weather_actual.csv")
compare = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\4_fcst_processed\round1_fcst_leak_deleted.csv')


# time 열을 datetime 형식으로 변환합니다
gens['time'] = pd.to_datetime(gens['time'])
actual['time'] = pd.to_datetime(actual['time'])
compare['time'] = pd.to_datetime(compare['time'])

# 1. gens
# 두 데이터프레임에서 중복되는 시간 데이터를 선택합니다 (gens, compare)
common_times_1 = set(gens['time']).intersection(set(compare['time']))

# 두 데이터프레임에서 공통된 시간 데이터만을 선택합니다
gens = gens[gens['time'].isin(common_times_1)]
compare = compare[compare['time'].isin(common_times_1)]


# 두 데이터프레임을 시간순으로 정렬합니다
gens = gens.sort_values(by='time')
compare = compare.sort_values(by='time')



# 2.actual
# 두 데이터프레임에서 중복되는 시간 데이터를 선택합니다 (actual, compare)
common_times_2 = set(actual['time']).intersection(set(compare['time']))

# 두 데이터프레임에서 공통된 시간 데이터만을 선택합니다
actual = actual[actual['time'].isin(common_times_2)]
compare = compare[compare['time'].isin(common_times_2)]


# 두 데이터프레임을 시간순으로 정렬합니다
actual = actual.sort_values(by='time')
compare = compare.sort_values(by='time')

# 저장
file_dir = (r"C:\Team3\Data\LSTM_binary\processed\5_gen,actual_leak_delete")

fcst_file_name_1 = "gens_leak_deleted.csv"
fcst_file_name_2 = "actual_leak_deleted.csv"

file_path_1 = os.path.join(file_dir, fcst_file_name_1)
file_path_2 = os.path.join(file_dir, fcst_file_name_2)

gens.to_csv(file_path_1, mode='w', index=False)
actual.to_csv(file_path_2, mode='w', index=False)
