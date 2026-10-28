import cv2
#Method 1#
image = cv2.imread(r'test.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, binary =cv2.threshold(gray, 80 , 255, cv2.THRESH_BINARY_INV)

cv2.imshow('BAW',binary)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Method 2#
# image = cv2.imread(r'test.jpg')
# import numpy as np
# lower_black = np.array([0,0,0])
# upper_black = np.array([90,90,90])

# mask = cv2.inRange(image, lower_black, upper_black)



# result = cv2.bitwise_and(image,image,mask=mask)

# white_bg = np.full_like(image, 255)
# final = np.where(mask[:, :, np.newaxis]==255, result, white_bg)

# cv2.imshow('Mask',final)
# cv2.waitKey(0)
# cv2.destroyAllWindows()