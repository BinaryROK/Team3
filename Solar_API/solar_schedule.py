import time
from Solar_API import bid_GBM as bid

import schedule

# 실행할 함수 정의


# 실행 시간 설정 (예: 오전 9시 15분)
desired_time = "09:15"

# 스케줄러 설정
schedule.every().day.at(desired_time).do(bid.solar_bid, "2023-11-5")

# 무한 루프에서 스케줄러 실행
while True:
    schedule.run_pending()
    time.sleep(60)  # 1분마다 스케줄러 확인
