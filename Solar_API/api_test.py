import requests
import json

import requests
import json
import params as pa
import pandas as pd
import os
from datetime import datetime, timedelta
import pytz
import solar_api as api

_API_URL = "https://research-api.solarkim.com"
_API_KEY = pa.SOLAR_APIKEY
_AUTH_PARAM = {"headers": {"Authorization": f"Bearer {_API_KEY}"}}

def _get(url: str):
    """
    주어진 url의 리소스를 조회한다.

    Args:
        url (str): API url
    """
    response = requests.get(url, **_AUTH_PARAM)
    return response.json()



Date = '2023-11-5'
df = pd.DataFrame(api._get_weather_fcst_10(Date))
df2 = pd.DataFrame(api._get_weather_fcst_17(Date))

#print(df)
print(df2)