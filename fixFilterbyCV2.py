import cv2
from cv2 import cvtColor, COLOR_BGR2RGB
import numpy as np
from numpy import array
import requests
import io
import PIL
from PIL import Image, ImageChops, ImageDraw, ImageFilter
import urllib.request
import matplotlib.pyplot as plt
import time
import requests
import schedule
'''
img1 = cv2.imread(r'D:\output\Radar_Image\Alert\original\rain.jpg')
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
print(img1.shape)
# Create mask
height,width,_ = img1.shape
mask = np.zeros((height,width), np.uint8)
cv2.circle(mask,(315,520),20,(255,255,255),thickness=-1)
# Copy that image using that mask
masked_data = cv2.bitwise_and(img1, img1, mask=mask)
# Apply Threshold
_,thresh = cv2.threshold(mask,1,255,cv2.THRESH_BINARY)
# Find Contour
contours,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
x,y,w,h = cv2.boundingRect(contours[0])
# Crop masked_data
crop = masked_data[y:y+h,x:x+w]
#filter image
img_hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
lower = np.array([0,118,156])
upper = np.array([100,255,255])
mask0 = cv2.inRange(img_hsv,lower, upper)
res = cv2.bitwise_and(crop,crop,mask=mask0)
#saveimage
cv2.imwrite(r'D:\output\Radar_Image\Alert\original\rainCompare.jpg',res)
#Code to close Window
cv2.imshow('Cropped Eye',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
#เปรียบเทียบรูปภาพ
img1 = Image.open(r'D:\output\Radar_Image\Alert\original\originalCompare.jpg')
img2 = Image.open(r'D:\output\Radar_Image\Alert\original\originalCompare.jpg')
# finding difference
diff = ImageChops.difference(img1, img2)
print(diff.getbbox())
    '''
    #img2 = img2[510:540,290:320]
    
    img_crop_8 = img2.crop((299,513,327,541))
    height8,width8 = img_crop_8.size
    lum_img_8 = Image.new('L',[height8,width8],0)
    draw = ImageDraw.Draw(lum_img_8)
    draw.pieslice([(0,0),(height8,width8)],0,360,fill=255,outline='white')
    img_arr = np.array(img_crop_8)
    lum_img_arr = np.array(lum_img_8)
    final_img_arr_8 = np.dstack((img_arr,lum_img_arr))

    
    final_img_arr_8[:,:,0] = np.ones([28,28])*64/255.0
    final_img_arr_8[:,:,1] = np.ones([28,28])*128/255.0
    final_img_arr_8[:,:,2] = np.ones([28,28])*192/255.0

    cv_img = final_img_arr_8.astype(np.uint8)
    cv_gray = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
    
    cv2.imwrite(r'C:\Users\BK\Desktop\autoLine\compare.jpg',cv_gray)
    
    '''
