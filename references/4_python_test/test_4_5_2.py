#2、中值滤波
import cv2
import copy
import random
import imutils
import numpy as np

img = cv2.imread('/home/mowen/4_python_test/test_4_5_pictures/test.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#给灰度图像自动添加椒盐噪音
pepper_img = copy.deepcopy(gray_img)
for i in range(gray_img.shape[0]):
    for j in range(gray_img.shape[1]):
        if random.randint(0, 20) == 0:
            pix = random.randint(250, 255)
            pepper_img[i, j] = pix

#opencv提供cv2.medianBlur()函数实现中值滤波
blur_img = cv2.medianBlur(pepper_img, 5)

#自实现中值滤波器
temp_arr = np.zeros((9))
median_img = copy.deepcopy(pepper_img)
for i in range(1, pepper_img.shape[0]-1):
    for j in range(1, pepper_img.shape[1]-1):
        temp_arr[0] = pepper_img[i-1, j-1]
        temp_arr[1] = pepper_img[i-1, j]
        temp_arr[2] = pepper_img[i-1, j+1]
        temp_arr[3] = pepper_img[i, j-1]
        temp_arr[4] = pepper_img[i, j]
        temp_arr[5] = pepper_img[i, j+1]
        temp_arr[6] = pepper_img[i+1, j-1]
        temp_arr[7] = pepper_img[i+1, j]
        temp_arr[8] = pepper_img[i+1, j+1]
        arr = np.sort(temp_arr)
        median_img[i, j] = arr[4]

cv2.imshow('pepper image', imutils.resize(pepper_img, 600))
cv2.imshow('blur image', imutils.resize(blur_img, 600))
cv2.imshow('median image', imutils.resize(median_img, 600))
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
