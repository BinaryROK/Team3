import pandas as pd
from datetime import timedelta
import API_weather
from CSV_weather_cut1 import process_weather_data1  # CSV_weather_cut1 모듈에서 함수를 가져옴
from CSV_weather_cut2 import process_weather_data2  # CSV_weather_cut2 모듈에서 함수를 가져옴
from API_uv_idx import get_and_save_uv_data
from CSV_uv_idx import process_uv_data_1
from CSV_uv_idx_final import process_uv_data_2
from API_sun import get_and_save_sun_data
from CSV_sun_cut import process_sun_data_1
from CSV_sun_interpolate import interpolate_sun_data
class WeatherData:
    def __init__(self, base_date, base_time, nx, ny, csv_file):
        self.base_date = base_date
        self.base_time = base_time
        self.nx = nx
        self.ny = ny
        self.csv_file = csv_file
class UVData:
    def __init__(self, base_date, base_time):
        self.base_date = base_date
        self.base_time = base_time

class SunDataRequest:
    def __init__(self, locdate, latitude, longitude, service_key):
        self.locdate = locdate
        self.latitude = latitude
        self.longitude = longitude
        self.service_key = service_key

def get_and_save_weather_data(weather_data):
    # API_weather 모듈의 get_weather_data와 save_to_csv 함수 호출
    header, data_rows = API_weather.get_weather_data(weather_data.base_date, weather_data.base_time, weather_data.nx, weather_data.ny)

    if header is not None and data_rows is not None:
        API_weather.save_to_csv(header, data_rows, weather_data.csv_file)

    else:
        print('Failed to retrieve or save data.')

def main():
    # 날씨 데이터를 가져오기 위한 WeatherData 객체 생성
    ################## base_date='20231217'라면 12월 18일 00시부터 20일 23시까지의 데이터가 받아와짐 뒷부분 불필요한 데이터는 합칠때 자름 ############
    weather_data = WeatherData(base_date='20231217', base_time='2300', nx='68', ny='111', csv_file='weather_data_1.csv')

    # get_and_save_weather_data 함수 호출
    get_and_save_weather_data(weather_data)

    # process_weather_data1 함수 호출 (CSV_weather_cut1 모듈에서 가져옴)
    process_weather_data1(r'C:\Team3\API_CSV\weather_data_1.csv', output_file_path='C:\Team3\API_CSV\weather_data_2.csv')

    # process_weather_data2 함수 호출 (CSV_weather_cut2 모듈에서 가져옴)
    process_weather_data2(r'C:\Team3\API_CSV\weather_data_2.csv', output_file_path='C:\Team3\API_CSV\weather_data_3.csv')

    # UVData 객체 생성 ######### base_date='20231218'라면 12월 18일 00시부터 20일 23시까지의 데이터가 받아와짐 뒷부분 불필요한 데이터는 합칠때 자름 ############
    uv_data = UVData(base_date='20231218', base_time='00')
    get_and_save_uv_data(uv_data.base_date, uv_data.base_time)

    process_uv_data_1(input_file_path=r'C:\Team3\API_CSV\uv_data_raw.csv', output_file_path=r'C:\Team3\API_CSV\uv_idx_3time.csv')

    process_uv_data_2(input_csv_path=r'C:\Team3\API_CSV\uv_idx_3time.csv', output_csv_path=r'C:\Team3\API_CSV\uv_idx_final.csv')

    # SunDataRequest 객체 생성 #######  locdate='20231220' 라면 12월20일 24시간 데이터만 뽑아준다 ###################
    sun_data_request = SunDataRequest(locdate='20231220', latitude='12659', longitude='3734',
                                      service_key='8gv6iLL5NMjLYTFifjbIh9yU4z/0xGYXgVgAJsYywpfYbMU1gCYAllIsVIrLEGM+DPi/NCXea0neY4fGRM2QmQ==')
    csv_file_path = r'C:\Team3\API_CSV\Sun_data_raw.csv'

    get_and_save_sun_data(sun_data_request.locdate, sun_data_request.latitude, sun_data_request.longitude,
                          csv_file_path)

    process_sun_data_1(input_csv_path=r'C:\Team3\API_CSV\Sun_data_raw.csv', output_csv_path=r'C:\Team3\API_CSV\Sun_data_cut.csv')

    interpolate_sun_data(input_csv_path=r'C:\Team3\API_CSV\Sun_data_cut.csv', output_csv_path=r'C:\Team3\API_CSV\Sun_data_interpolate.csv')


# main 함수 호출
if __name__ == "__main__":
    main()
