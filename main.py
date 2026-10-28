import time
import schedule
import logging
from rain_checker import checkImg
from lineAlert import rainy
import os
# ตั้งค่า logging
log_path = os.path.join(os.path.dirname(__file__), "rain.log")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
def wait_until_rain_stops():
    logging.info("เข้าสู่โหมดรอฝนหยุด")
    #print("📌 เข้าสู่โหมดติดตามฝน (loop ทุก 15 นาที)...")
    while True:
        time.sleep(1800)
        rain_status, directions, check_time = checkImg()
        if rain_status:
            msg = f"☔ ยังมีฝน: {rain_status} | ทิศทาง: {', '.join(directions.keys())}| เวลา:{check_time}"
            #print(msg)
            logging.info(msg)
            
        else:
            logging.info("✅ ฝนหยุดแล้ว ออกจากลูป")
            print("✅ ฝนหยุดแล้ว! กลับไปทำงานปกติ")
            break

def scheduled_check():
    rain_status, directions, check_time = checkImg()
    if rain_status:
        msg = f"🔔  พบฝน: {rain_status} | ทิศทาง: {', '.join(directions.keys())} | เวลา:{check_time}"
        print(msg)
        logging.warning(msg)  # ใช้ WARNING เพื่อเน้น
        rainy(msg)
        wait_until_rain_stops()
    else:
        logging.info("[Schedule] 🌤️ ไม่มีฝน")
        print("[Schedule] 🌤️ ไม่มีฝน")
# เรียกครั้งแรกก่อน
scheduled_check()
schedule.every(30).minutes.do(scheduled_check)
# รอ schedule ทำงานทุก 15 นาที
while True:
    schedule.run_pending()
    time.sleep(1)
