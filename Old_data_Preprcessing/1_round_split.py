import os
import pandas as pd


# 5개모델 pred.csv를 round1,2로 분리하는코드
# CSV 파일을 불러오기
df = pd.read_csv('C:\Team3\Data\LSTM_binary\pred.csv')

# 'round' 열의 고유 값 확인
unique_rounds = df['round'].unique()

# 각 'round' 값에 대해 데이터를 분리하고 별도의 CSV 파일로 저장
for round_value in unique_rounds:
    # 'round' 값에 따라 데이터 필터링
    filtered_data = df[df['round'] == round_value]

    # CSV 파일 이름 설정
    file_name = f'round_{round_value}.csv'
    file_dir = (r"C:\Team3\Data\LSTM_binary\processed\1_round_split")
    file_path = os.path.join(file_dir,file_name)

    filtered_data.to_csv(file_path, mode = 'w' ,index=False)
