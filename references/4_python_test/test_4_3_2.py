#2、加权平均法(w_average)
import cv2
image = cv2.imread('/home/mowen/4_python_test/test_4_3_pictures/2.jpg',cv2.IMREAD_COLOR)
cv2.imshow('2.jpg',image)
new = image.copy()
height, width, channels = image.shape
for i in range(height):
        for j in range(width):
            new[i,j] = 0.3 * int(image[i,j][0]) + 0.59 * int(image[i,j][1]) + 0.11 *int(image[i,j][2])
cv2.imshow('result',new)
cv2.waitKey(0)