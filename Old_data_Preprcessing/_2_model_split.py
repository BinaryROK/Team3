import pandas as pd
import os


# 분리된round1,2를 모델1~5를 열로 만들어서 정렬하기
# CSV 파일을 불러오기
df1 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\1_round_split\round_1.csv')
df2 = pd.read_csv(r'C:\Team3\Data\LSTM_binary\processed\1_round_split\round_2.csv')

# 'model_id'를 열로 사용하여 데이터 변환
df1 = df1.pivot(index=['round', 'time'], columns='model_id', values='amount').reset_index()
df2 = df2.pivot(index=['round', 'time'], columns='model_id', values='amount').reset_index()

# 열 이름을 수정하여 'model_1', 'model_2', 등으로 변경합니다
df1.columns = [f'model_{col}' if col != ('round', 'time') else col for col in df1.columns]
df2.columns = [f'model_{col}' if col != ('round', 'time') else col for col in df2.columns]

# 열 이름을 원하는대로 변경

df1.columns = ['round', 'time', 'model_1', 'model_2', 'model_3', 'model_4', 'model_5']
df2.columns = ['round', 'time', 'model_1', 'model_2', 'model_3', 'model_4', 'model_5']
# 결과를 CSV 파일로 저장할 수도 있습니다

file_dir = (r"C:\Team3\Data\LSTM_binary\processed\2_model_split")
file_name_1 = "round_1_model_splitted.csv"
file_name_2 = "round_2_model_splitted.csv"

file_path_1 = os.path.join(file_dir, file_name_1)
file_path_2 = os.path.join(file_dir, file_name_2)

df1.to_csv(file_path_1, mode='w', index=False)
df2.to_csv(file_path_2, mode='w', index=False)

def model_split(df):
    df = df.pivot(index=['round', 'time'], columns='model_id', values='amount').reset_index()
    df.columns = [f'model_{col}' if col != ('round', 'time') else col for col in df.columns]
    df.columns = ['round', 'time', 'model_1', 'model_2', 'model_3', 'model_4', 'model_5']

    return df

def model_split_pred(df):
    df = df.pivot(index=[ 'time'], columns='model_id', values='amount').reset_index()
    df.columns = [f'model_{col}' if col != ('round', 'time') else col for col in df.columns]
    df.columns = ['round', 'time', 'model_1', 'model_2', 'model_3', 'model_4', 'model_5']

    return df