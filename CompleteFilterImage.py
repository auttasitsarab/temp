import cv2
import numpy as np
import matplotlib.pyplot as plt
import colorsys

img =cv2.imread(r'D:\autoLineAlert\test.jpg')
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0,118,156])
upper = np.array([100,255,255])
mask0 = cv2.inRange(img_hsv,lower, upper)
res = cv2.bitwise_and(img,img,mask=mask0)
cv2.imwrite('filterImage.jpg',res)


