import cv2
import numpy as np
import matplotlib.pyplot as plt
import colorsys

img =cv2.imread(r'D:\autoLineAlert\test.jpg')
img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

def rgb_hsv_converter(rgb):
    (r,g,b) = rgb_normalizer(rgb)
    hsv = colorsys.rgb_to_hsv(r,g,b)
    (h,s,v) = hsv_normalizer(hsv)
    upper_band = [h+10, s+40, v+40]
    lower_band = [h-10, s-40, v-40]
    return {
        'upper_band': upper_band,
        'lower_band': lower_band
    }

def rgb_normalizer(rgb):
    (r,g,b) = rgb
    return (r/255, g/255, b/255)

def hsv_normalizer(hsv):
    (h,s,v) = hsv
    return (h*360, s*255, v*255)

#rgb_hsv_converter((247,247,0))

import cv2
import numpy as np

def nothing(x):
    pass

# Load image
img =cv2.imread(r'D:\autoLineAlert\test.jpg')

# Create a window
cv2.namedWindow('img')

# Create trackbars for color change
# Hue is from 0-179 for Opencv
cv2.createTrackbar('HMin', 'img', 0, 179, nothing)
cv2.createTrackbar('SMin', 'img', 0, 255, nothing)
cv2.createTrackbar('VMin', 'img', 0, 255, nothing)
cv2.createTrackbar('HMax', 'img', 0, 179, nothing)
cv2.createTrackbar('SMax', 'img', 0, 255, nothing)
cv2.createTrackbar('VMax', 'img', 0, 255, nothing)

# Set default value for Max HSV trackbars
cv2.setTrackbarPos('HMax', 'img', 179)
cv2.setTrackbarPos('SMax', 'img', 255)
cv2.setTrackbarPos('VMax', 'img', 255)

# Initialize HSV min/max values
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

while(1):
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'img')
    sMin = cv2.getTrackbarPos('SMin', 'img')
    vMin = cv2.getTrackbarPos('VMin', 'img')
    hMax = cv2.getTrackbarPos('HMax', 'img')
    sMax = cv2.getTrackbarPos('SMax', 'img')
    vMax = cv2.getTrackbarPos('VMax', 'img')

    # Set minimum and maximum HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Convert to HSV format and color threshold
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    # Print if there is a change in HSV value
    if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    # Display result image
    cv2.imshow('img', result)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()