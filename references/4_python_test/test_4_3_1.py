#1、平均值法(average)
import cv2
image = cv2.imread('/home/mowen/4_python_test/test_4_3_pictures/1.jpg',cv2.IMREAD_COLOR)
cv2.imshow('1.jpg',image)
new = image.copy()
height, width, channels = image.shape
for i in range(height):
    for j in range(width):
            new[i,j] = (int(image[i,j][0]) + int(image[i,j][1]) + int(image[i,j][2]))/3
cv2.imshow('result',new)
cv2.waitKey(0)