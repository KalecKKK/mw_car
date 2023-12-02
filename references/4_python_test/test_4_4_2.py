#2、彩色图像直方图
import cv2
import numpy as np
#计算每个通道的直方图函数
def calcAndDrawHist(image, color):
    hist= cv2.calcHist([image], [0], None, [256], [0.0,255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    histImg = np.zeros([256,256,3], np.uint8)
    hpt = int(0.9* 256);
    for h in range(256):
        intensity = int(hist[h]*hpt/maxVal)
        cv2.line(histImg,(h,256), (h,256-intensity), color)
    return histImg;
img = cv2.imread('/home/mowen/4_python_test/test_4_3_pictures/3.jpg',cv2.IMREAD_COLOR)
b, g, r = cv2.split(img)
histImgB = calcAndDrawHist(b, [255, 0, 0])
histImgG = calcAndDrawHist(g, [0, 255, 0])
histImgR = calcAndDrawHist(r, [0, 0, 255])
hisimg = np.hstack((histImgB,histImgG,histImgR))
cv2.imshow("HIST", hisimg)
cv2.imshow("Img", img)
cv2.waitKey(0)