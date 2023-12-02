import cv2
import numpy as np

img = cv2.imread('/home/mowen/4_python_test/test_4_7_files/20210706221702710.png')
P = [[458.654, 0, 367.215],
     [0, 457.296, 248.375],
     [0, 0, 1]]
K = [-0.28340811, 0.07395907, 0.00019359, 1.76187114e-05]
img_distort = cv2.undistort(img, np.array(P), np.array(K))
img_diff = cv2.absdiff(img, img_distort)
cv2.imshow('img', img)
cv2.imshow('img_distort', img_distort)
cv2.waitKey(0)

