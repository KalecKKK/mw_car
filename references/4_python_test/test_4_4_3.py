#3、图像直方图均衡化
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


def hisEqulColor(img):
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return img


img1 = cv2.imread('/home/mowen/4_python_test/test_4_3_pictures/3.jpg',cv2.IMREAD_COLOR)
img = img1.copy()
b1, g1, r1 = cv2.split(img)
histImgB1 = calcAndDrawHist(b1, [255, 0, 0])
histImgG1 = calcAndDrawHist(g1, [0, 255, 0])
histImgR1 = calcAndDrawHist(r1, [0, 0, 255])
equ = hisEqulColor(img)
b2, g2, r2 = cv2.split(equ)
histImgB2 = calcAndDrawHist(b2, [255, 0, 0])
histImgG2 = calcAndDrawHist(g2, [0, 255, 0])
histImgR2 = calcAndDrawHist(r2, [0, 0, 255])
res = np.vstack((img1,equ))
cv2.imshow('result',res)
his_b_res = np.vstack((histImgB1,histImgB2))
his_g_res = np.vstack((histImgG1,histImgG2))
his_r_res = np.vstack((histImgR1,histImgR2))
hisres = np.hstack((his_b_res,his_g_res,his_r_res))
cv2.imshow('hisres',hisres)
cv2.waitKey(0)