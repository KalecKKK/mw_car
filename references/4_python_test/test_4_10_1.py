import cv2
import numpy as np
import math
img=cv2.imread("/home/mowen/4_python_test/test_4_10_data/222.jpg")


def celiang(img1):
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray, (3, 3), 0)
    cv2.imshow("gaosi",blur)
    edged = cv2.Canny(blur, 70, 80)
    lunkuo(edged,img1)
    cv2.imshow("edged",edged)
    cv2.imshow("img",img1)

# img2为二值化图，img3为原图
def lunkuo(img2,img3):
    binary,cnts, hierarchy = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 标记尺寸格在左上角，先寻找左上角的尺寸格
    # 遍历每一个轮廓，计算平均x,y坐标值，最小的则为标记格
    ar_min=[]
    for lun in range(len(cnts)):
        # 最小外接矩形
        rect = cv2.minAreaRect(cnts[lun])
        x=int((int(rect[0][0])+int(rect[1][0]))/2)
        y = int((int(rect[0][1]) + int(rect[1][1])) / 2)
        x_y=x+y
        ar_min.append(x_y)
    # 求列表最小值及索引
    min_value = min(ar_min)  # 求列表最小值
    min_idx =ar_min.index(min_value) # 求最小值对应索引
    # 标记格两点的实际距离为2.8
    # 标记格两点的像素距离的二次方为long
    rect1=cv2.minAreaRect(cnts[min_idx])
    box_1 = cv2.boxPoints(rect1)
    # 数据类型转换
    box_biao = np.int0(box_1)
    cha_x=abs(int(box_biao[0][0])-int(box_biao[2][0]))
    cha_y=abs(int(box_biao[0][1])-int(box_biao[2][1]))
    cv2.line(img3, (int(box_biao[0][1]), int(box_biao[0][0])), (int(box_biao[2][1]), int(box_biao[2][0])), (0, 255, 0), 2)
    long=int((cha_x*cha_x)+(cha_y*cha_y))
    long1=math.sqrt(long)
    for lun in range(len(cnts)):
        # 最小外接矩形
        rect = cv2.minAreaRect(cnts[lun])
        box = cv2.boxPoints(rect)
        # 数据类型转换
        box1 = np.int0(box)
        # 计算两条边的长度

        bian1=int((abs(box1[0][0]-box1[1][0])*abs(box1[0][0]-box[1][0]))+(abs(box1[0][1]-box1[1][1])*abs(box1[0][1]-box1[1][1])))
        bian2 = int((abs(box1[0][0] - box1[-1][0]) * abs(box1[0][0] - box1[-1][0])) + (
                    abs(box1[0][1] - box1[-1][1]) * abs(box1[0][1] - box1[-1][1])))
        bian11=math.sqrt(bian1)
        bian22=math.sqrt(bian2)
        # 转换实际距离
        bian1_shiji = (2.8 / long1) * bian11
        bian_shiji_1 = round(bian1_shiji, 2)
        bian2_shiji = (2.8 / long1) * bian22
        bian_shiji_2 = round(bian2_shiji, 2)
        cv2.drawContours(img3, [box1], -1, (0, 0, 255), 2)  # 画出各个轮廓

        cv2.line(img3, (int(box1[0][0]), int(box1[0][1])), (int(box1[1][0]), int(box1[1][1])), (255, 0, 0), 2)
        cv2.putText(img3, str(bian_shiji_1),(int(box1[1][0])-30,int(box1[1][1])+30),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

        cv2.line(img3, (int(box1[0][0]), int(box1[0][1])), (int(box1[-1][0]), int(box1[-1][1])), (255, 0, 0), 2)
        cv2.putText(img3, str(bian_shiji_2),(int(box1[-1][0])-30,int(box1[-1][1])+30),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

if __name__ == '__main__':
     celiang(img)

cv2.waitKey(0)
