import cv2
import numpy as np
image = cv2.imread(r"D:\autoLineAlert\test.jpg")
print(image.shape)
image = cv2.resize(image,(400,400))
print(image.shape)

def clickPosition(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        text = str(x)+','+str(y)
        cv2.putText(image,text,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),cv2.LINE_4)
        cv2.imshow('output',image)

cv2.imshow('output',image)
cv2.setMouseCallback('output',clickPosition)
cv2.waitKey(0)
cv2.destroyAllWindows()

y=36
x=13
h=400
w=379
crop_image = image[x:w, y:h]
cv2.imshow("Cropped", crop_image)
cv2.imwrite('output.jpg',crop_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



