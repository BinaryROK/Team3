import pandas as pd
import numpy as np
import requests
import json
import params as pa
import solar_api as api
from Model.Model_saved import gen as g
import os
from datetime import datetime



Date = "2023-11-2"

df = pd.DataFrame(api._get_weather_fcst_10(Date))

filename = "WeatherData_"+ Date

DataPath = os.path.join("C:\Team3\Data\Test", filename)
df.to_csv()
df.to_csv(DataPath, index=False)

result_df = g.gen(DataPath)


result_list = result_df['Predicted'].tolist()
