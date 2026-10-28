import cv2
import numpy as np
import requests
import io
import PIL
from PIL import Image, ImageChops, ImageDraw
import urllib.request
import matplotlib.pyplot as plt
import time
import requests
import schedule
import lineAlert
def checkImg():
    #กำหนดตัวแปรต่างๆ
    date_string = time.strftime('%Y%m%d%H%M')
    dirOriginal = r'D:\output\alert\original\originalCompare.jpg'
    dirNew = r'D:\output\alert\new\\'
    url = r'https://weather.tmd.go.th/cmp/cmp240_latest.gif'

    #โหลดรูปภาพ
    img2 = Image.open(requests.get(url,stream=True).raw)
    
    #เปลี่ยนให้เป็นjpg
    rgb_im = img2.convert('RGB')
    rgb_im.save(dirNew+date_string+'.jpg')
    
    #Crop    
    img2 = cv2.imread(dirNew+date_string+'.jpg')
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    # Create mask
    height,width,_ = img2.shape
    mask = np.zeros((height,width), np.uint8)
    cv2.circle(mask,(315,520),20,(255,255,255),thickness=-1)
    # Copy that image using that mask
    masked_data = cv2.bitwise_and(img2, img2, mask=mask)
    # Apply Threshold
    _,thresh = cv2.threshold(mask,1,255,cv2.THRESH_BINARY)
    # Find Contour
    contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = cv2.boundingRect(contours[0])
    # Crop masked_data
    crop = masked_data[y:y+h,x:x+w]
    cv2.imwrite(dirNew+'crop.jpg',crop)
    #filter image
    img_hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    lower = np.array([0,118,156])
    upper = np.array([100,255,255])
    mask0 = cv2.inRange(img_hsv,lower, upper)
    res = cv2.bitwise_and(crop,crop,mask=mask0)
    
    cv2.imwrite(dirNew+'img2.jpg',res)

    #เปรียบเทียบรูปภาพ
    img1 = Image.open(dirOriginal)
    img2 = Image.open(r'D:\output\alert\new\img2.jpg')
    # finding difference
    diff = ImageChops.difference(img1, img2)
    if diff.getbbox():
        print('different')
        lineAlert.rainy()
        while True:
            print('onLoop')
            time.sleep(900)            
            new_date_string = time.strftime('%Y%m%d%H%M')
            img = Image.open(requests.get(url,stream=True).raw)
            rgb_im = img.convert('RGB')
            rgb_im.save(dirNew+new_date_string+'.jpg')
            img2 = cv2.imread(dirNew+new_date_string+'.jpg')
            img2 = img2[510:540,290:320]
            
            #filter image
            img_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
            lower = np.array([0,118,156])
            upper = np.array([100,255,255])
            mask0 = cv2.inRange(img_hsv,lower, upper)
            res = cv2.bitwise_and(img2,img2,mask=mask0)

            #clearBackgroud
            tmp = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
            _, alpha = cv2.threshold(tmp,0,255,cv2.THRESH_OTSU)
            b, g, r = cv2.split(res)
            rgba=[b,g,r,alpha]
            src = cv2.merge(rgba,4)
            cv2.imwrite(dirNew+'img2.jpg',src)

            #เปรียบเทียบรูปภาพ
            img1 = Image.open(dirOriginal)
            img2 = Image.open(r'D:\output\Alert\new\img2.jpg')
            diff = ImageChops.difference(img1, img2)
            
            if diff.getbbox() == None:
                break
        print('outttt')
    else:
        print('same')

checkImg()
schedule.every(15).minutes.do(checkImg)
while True:
    schedule.run_pending()
    time.sleep(1)
