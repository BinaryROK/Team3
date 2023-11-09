from Solar_API import solar_api as api
import pandas as pd
from Old_data_Preprcessing import _2_model_split as ms

def input_10(Date):
    file_name = 'WeatherData_' + Date
    fcst = api._get_weather_fcst_10(Date)
    pred = api._get_gen_forecasts_10(Date)
    fcst['model_1'] = pred['model1']
    fcst['model_2'] = pred['model2']
    fcst['model_3'] = pred['model3']
    fcst['model_4'] = pred['model4']
    fcst['model_5'] = pred['model5']
    fcst['cloud_1'] = fcst['cloud']
    fcst['temp_1'] = fcst['temp']
    fcst['humidity_1'] = fcst['humidity']
    fcst['ground_press_1'] = fcst['ground_press']
    fcst['wind_speed_1'] = fcst['wind_speed']
    fcst['wind_dir_1'] = fcst['wind_dir']
    fcst['rain_1'] = fcst['rain']
    fcst['snow_1'] =fcst['snow']
    fcst['dew_point_1'] = fcst['dew_point']
    fcst['vis_1'] = fcst['vis']
    fcst['uv_idx_1'] = fcst['uv_idx']
    fcst['azimuth_1'] = fcst['azimuth']
    fcst['elevation_1'] = fcst['elevation']


    train_x = fcst



    return train_x

def input_17(Date):
    file_name = 'WeatherData_' + Date
    fcst = api._get_weather_fcst_17(Date)
    pred = api._get_gen_forecasts_17(Date)
    fcst['model_1'] = pred['model1']
    fcst['model_2'] = pred['model2']
    fcst['model_3'] = pred['model3']
    fcst['model_4'] = pred['model4']
    fcst['model_5'] = pred['model5']
    fcst['cloud_1'] = fcst['cloud']
    fcst['temp_1'] = fcst['temp']
    fcst['humidity_1'] = fcst['humidity']
    fcst['ground_press_1'] = fcst['ground_press']
    fcst['wind_speed_1'] = fcst['wind_speed']
    fcst['wind_dir_1'] = fcst['wind_dir']
    fcst['rain_1'] = fcst['rain']
    fcst['snow_1'] =fcst['snow']
    fcst['dew_point_1'] = fcst['dew_point']
    fcst['vis_1'] = fcst['vis']
    fcst['uv_idx_1'] = fcst['uv_idx']
    fcst['azimuth_1'] = fcst['azimuth']
    fcst['elevation_1'] = fcst['elevation']


    train_x = fcst



    return train_x


Date = '2023-11-09'
input_10(Date)
print(input_10(Date))
