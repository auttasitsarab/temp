import numpy as np
from collections import Counter, defaultdict
import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import math
from datetime import datetime

def crop_circle_grayscale(image_path, center, radius, output_path):
    """
    ครอบภาพ grayscale แบบวงกลมจากพิกัดและรัศมีที่กำหนด
    
    :param image_path: path ภาพต้นฉบับ
    :param center: (x, y) จุดศูนย์กลางของวงกลม
    :param radius: รัศมีวงกลม (พิกเซล)
    :param output_path: บันทึกไฟล์ หรือ None เพื่อแสดงอย่างเดียว
    """
    # เปิดและแปลงภาพเป็น grayscale ('L')
    img = Image.open(image_path).convert("L")
    cx, cy = center
    left = cx - radius
    top = cy - radius
    right = cx + radius
    bottom = cy + radius

    # ครอบสี่เหลี่ยมรอบวงกลม
    img_cropped = img.crop((left, top, right, bottom))

    # สร้าง mask วงกลม
    mask = Image.new('L', (2 * radius, 2 * radius), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 2 * radius, 2 * radius), fill=255)

    # รวม grayscale กับ mask เป็นภาพ RGBA (เพื่อให้พื้นหลังโปร่งใส)
    img_result = Image.new("LA", (2 * radius, 2 * radius))  # L = grayscale, A = alpha
    img_result.putalpha(mask)
    img_result.paste(img_cropped, (0, 0), mask)
        # แปลงจากภาพ grayscale ที่มี alpha (mode='LA') → pure grayscale
    #img_result = img_result.convert('L')

    # บันทึกหรือแสดง
    if output_path:
        img_result.save(output_path)
    else:
        img_result.show()

    return img_result

def direction_code(center, point, tolerance=5):
    import math
    dy = center[0] - point[0]  # ระยะในแกน Y (กลับด้าน เพราะภาพ y คว่ำ)
    dx = point[1] - center[1]  # ระยะในแกน X

    distance = math.hypot(dx, dy)
    if distance <= tolerance:
        return "OverAD"

    angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360  # มุม 0-360

    directions = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
    index = int(((angle + 22.5) % 360) // 45)
    return directions[index]



def checkImg(folder_path=r'D:\forecast\ranongCappi\\'):
    # 1. หาไฟล์ภาพล่าสุดในโฟลเดอร์
    valid_exts = ['.jpg', '.jpeg', '.png']
    files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in valid_exts]
    if not files:
        print("⚠️ ไม่พบไฟล์ภาพในโฟลเดอร์")
        return None, {}

    # 2. เลือกไฟล์ที่แก้ไขล่าสุด
    files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    latest_file = os.path.join(folder_path, files[0])
    time_str = latest_file[-21:-17]

    # แปลงเป็น datetime แล้วฟอร์แมต
    time_obj = datetime.strptime(time_str, "%H%M")
    formatted_time = time_obj.strftime("%H:%M")
    formatted_time = formatted_time + ' UTC'

    print(f"🖼️ latest_file: {latest_file}")

    img_cropped = crop_circle_grayscale(latest_file, center=(392, 433), radius=13, output_path=r"D:\autoLineAlert\circle_gray.png")
    gray = np.array(img_cropped.convert('L'))
    center = np.array(gray.shape) // 2

    rain_levels = [
        (200, 256, "Heavy Rain"),
        (130, 200, "Moderate Rain"),
        (30, 130, "Light Rain")
    ]

    rain_directions = defaultdict(Counter)
    found_levels = []

    for lower, upper, label in rain_levels:
        mask = (gray > lower) & (gray <= upper)
        if np.any(mask):
            positions = np.argwhere(mask)
            directions = [direction_code(center, pos) for pos in positions]
            count = Counter(directions)
            rain_directions[label] = count
            found_levels.append(label)

    # Return the strongest rain level if found
    for _, _, label in rain_levels:
        if label in rain_directions:
            return label, rain_directions[label], formatted_time

    return None, {}, formatted_time

def direction_code_gemini(center, point, tolerance=5):
    dy = center[0] - point[0]  # ระยะในแกน Y (กลับด้าน เพราะภาพ y คว่ำ)
    dx = point[1] - center[1]  # ระยะในแกน X

    distance = math.hypot(dx, dy)
    if distance <= tolerance:
        return "OverAD"

    angle = math.degrees(math.atan2(dy, dx)) # คำนวณองศา
    angle = (angle + 360) % 360 # ทำให้เป็น 0-359.99... เสมอ

    # แบ่งเป็น 8 ทิศ ทุก 45 องศา (กลางคือ ±22.5)
    # จุดกึ่งกลางของแต่ละทิศ: E=0, NE=45, N=90, NW=135, W=180, SW=225, S=270, SE=315
    
    # กำหนดขอบเขตของแต่ละทิศ
    if (angle >= 337.5 or angle < 22.5):
        return "E"
    elif (angle >= 22.5 and angle < 67.5):
        return "NE"
    elif (angle >= 67.5 and angle < 112.5):
        return "N"
    elif (angle >= 112.5 and angle < 157.5):
        return "NW"
    elif (angle >= 157.5 and angle < 202.5):
        return "W"
    elif (angle >= 202.5 and angle < 247.5):
        return "SW"
    elif (angle >= 247.5 and angle < 292.5):
        return "S"
    elif (angle >= 292.5 and angle < 337.5):
        return "SE"