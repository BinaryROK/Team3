import os
import pandas as pd



# pred round1 2를 fcst의 time과 수일치시키기
test_x = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\5_gen,actual_leak_delete\actual_leak_deleted.csv') #11577
test_y = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\5_gen,actual_leak_delete\gens_leak_deleted.csv') #11577

train_x_1 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\4_fcst_processed\round1_fcst_leak_deleted.csv') #11577
train_x_2 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\4_fcst_processed\round2_fcst_leak_deleted.csv') #11577

train_y_1 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\6_pred_leak_deleted\pred_round1.csv') # 11592
train_y_2 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\6_pred_leak_deleted\pred_round2.csv') # 11592

# time 열을 datetime 형식으로 변환합니다
train_y_1['time'] = pd.to_datetime(train_y_1['time'])
train_y_2['time'] = pd.to_datetime(train_y_2['time'])

train_x_1['time'] = pd.to_datetime(train_x_1['time'])
train_x_2['time'] = pd.to_datetime(train_x_2['time'])

test_x['time'] = pd.to_datetime(test_x['time'])
test_y['time'] = pd.to_datetime(test_y['time'])



# 1. train_y_1
# 두 데이터프레임에서 중복되는 시간 데이터를 선택합니다 (gens, compare)
common_times_1 = set(train_y_1['time']).intersection(set(train_x_1['time']))

# 두 데이터프레임에서 공통된 시간 데이터만을 선택합니다
train_y_1 = train_y_1[train_y_1['time'].isin(common_times_1)]
train_x_1 = train_x_1[train_x_1['time'].isin(common_times_1)]


# 두 데이터프레임을 시간순으로 정렬합니다
train_y_1 = train_y_1.sort_values(by='time') #11569
train_x_1 = train_x_1.sort_values(by='time')



# 2.train_y_2
# 두 데이터프레임에서 중복되는 시간 데이터를 선택합니다 (actual, compare)
common_times_2 = set(train_y_2['time']).intersection(set(train_x_1['time']))

# 두 데이터프레임에서 공통된 시간 데이터만을 선택합니다
train_y_2 = train_y_2[train_y_2['time'].isin(common_times_2)]
train_x_1 = train_x_1[train_x_1['time'].isin(common_times_2)]


# 두 데이터프레임을 시간순으로 정렬합니다
train_y_2 = train_y_2.sort_values(by='time')#11569
train_x_1 = train_x_1.sort_values(by='time')#11569


# test_y  정렬
test_y = test_y[test_y['time'].isin(common_times_2)]
test_y = test_y.sort_values(by='time')

# test_x 정렬
test_x = test_x[test_x['time'].isin(common_times_2)]
test_x = test_x.sort_values(by='time')

# test_x_2정렬
train_x_2 = train_x_2[train_x_2['time'].isin(common_times_2)]
train_x_2 = train_x_2.sort_values(by='time')









# 저장
file_dir = (r"C:\Team3\Data\LSTM_binary\processed\7_input_data")

train_y_1.to_csv(os.path.join(file_dir,'train_y_1.csv'), mode='w', index=False)
train_y_2.to_csv(os.path.join(file_dir,'train_y_2.csv'), mode='w', index=False)

test_x.to_csv(os.path.join(file_dir,'text_x.csv'), mode='w', index=False)
test_y.to_csv(os.path.join(file_dir,'test_y.csv'), mode='w', index=False)

train_x_1.to_csv((os.path.join(file_dir,'train_x_1.csv')), mode='w',index=False)
train_x_2.to_csv((os.path.join(file_dir,'train_x_2.csv')), mode='w',index=False)

