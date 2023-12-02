#1、均值滤波
import cv2
import copy
import random
import imutils
import numpy as np

img = cv2.imread('/home/mowen/4_python_test/test_4_5_pictures/test.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#利用 opencv 提供函数实现均值滤波
blur_img = cv2.blur(gray_img, (3, 3))

#在灰度图上手动实现均值滤波器
gray_avg_img = copy.deepcopy(gray_img)
for i in range(1, gray_img.shape[0]-1):
    for j in range(1, gray_img.shape[1]-1):
        sum_pix = sum([gray_img[l, k] for l in range(i-1, i+2) for k in range(j-1, j+2)])
        gray_avg_img [i, j] = int(sum_pix/9)

#在 RGB 彩色图上手动实现均值滤波器
rgb_avg_img = copy.deepcopy(img)
for i in range(1, img.shape[0]-1):
    for j in range(1, img.shape[1]-1):
        sum_b_pix = sum([img[l, k, 0] for l in range(i-1, i+2) for k in range(j-1, j+2)])
        sum_g_pix = sum([img[l, k, 1] for l in range(i-1, i+2) for k in range(j-1, j+2)])
        sum_r_pix = sum([img[l, k, 2] for l in range(i-1, i+2) for k in range(j-1, j+2)])
        rgb_avg_img [i, j] = [int(sum_b_pix/9), int(sum_g_pix/9), int(sum_r_pix/9)]

cv2.imshow('origin image', imutils.resize(img, 500))
cv2.imshow('gray image', imutils.resize(gray_img, 500))
cv2.imshow('blur image', imutils.resize(blur_img, 500))
cv2.imshow('gray average image', imutils.resize(gray_avg_img , 500))
cv2.imshow('rgb average  image', imutils.resize(rgb_avg_img , 500))
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
