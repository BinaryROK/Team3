import requests
import json
import requests
import pprint
import requests
from urllib.request import urlopen



import requests

# API 키와 요청할 URL 설정
apiKey = "0rTsyU1wQy-07MlNcAMvPw"
url_time = "https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?tm=202211300900&stn=0&help=0&authKey=0rTsyU1wQy-07MlNcAMvPw"

with urlopen(url_time) as f:
    html = f.read()
    print(html)