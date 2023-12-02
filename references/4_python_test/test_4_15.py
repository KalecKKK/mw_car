# 情绪异常检测
import dlib
import numpy as np
import cv2
# 导入正则表达式模块
import re


def jiance(img):
    img_hua=img.copy()

    #  灰度转换
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 加载模型
    # 正向人脸检测
    detector = dlib.get_frontal_face_detector()
    ad=detector(gray,1)
    if len(ad)>0:
        string = str(ad[0])

        # 含有数字的字符串（可以看到有小数和整数）
        # 获取所有数字
        # print(re.findall(r"\d+", string))
        wz = re.findall(r"\d+", string)

        cv2.rectangle(img_hua, (int(wz[0]), int(wz[1])), (int(wz[2]), int(wz[3])), (255, 255, 255), 2)
        # cv2.imshow("hua",img_hua)
        # 人脸关键点检测器
        predictor = dlib.shape_predictor(
            "/home/mowen/4_python_test/test_4_8_data/data_dlib/shape_predictor_68_face_landmarks.dat")
        # print(len(ad))
        # 利用预测器预测

        # 分别计算嘴张开的高度和宽度于脸部的高度和宽度的比例判断是否微笑
        # 脸的高度采用点9和28两点的距离，宽采用4和13两点的距离
        # 嘴张开的高度采用点52和58两点的距离，宽采用49和55两点的距离
        long_f = []  # 依次记录9，28，4，13的位置

        long_m = []  # 依次记录52，58，49，55的位置
        for i in range(len(ad)):
            landmarks = np.matrix([[p.x, p.y] for p in predictor(img, ad[i]).parts()])
            for idx, point in enumerate(landmarks):
                # 68点的坐标
                pos = (point[0, 0], point[0, 1])
                # print(idx, pos)
                if idx == 9:
                    long_f.append(pos[1])
                if idx == 28:
                    long_f.append(pos[1])
                if idx == 4:
                    long_f.append(pos[0])
                if idx == 13:
                    long_f.append(pos[0])
                ###########################################
                if idx == 52:
                    long_m.append(pos[1])
                if idx == 58:
                    long_m.append(pos[1])
                if idx == 49:
                    long_m.append(pos[0])
                if idx == 55:
                    long_m.append(pos[0])
                # 利用cv2.circle给每个特征点画一个圈，共68个
                # cv2.circle(img_hua, pos, 5, color=(0, 255, 0))
                # 利用cv2.putText输出1-68
                # font = cv2.FONT_HERSHEY_SIMPLEX
                # cv2.putText(img_hua, str(idx + 1), pos, font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        # long_f存储为4x,9y,13x,28y
        # long_m存储为49x,52x,55y,58y
        # print(long_f)
        # print(long_m)
        # 脸高
        f_g = float(long_f[1] - long_f[3])
        # print(f_g)
        # 脸宽
        f_k = float(long_f[2] - long_f[0])
        # print(f_k)

        # 嘴高
        z_g = long_m[3] - long_m[1]
        # print(z_g)
        # 嘴宽
        z_k = long_m[2] - long_m[0]
        # print(z_k)

        # b_g = round(z_g / f_g, 3)
        # print("kuan:", b_g)
        # b_k = round(z_k / f_k, 3)
        # print("gao", b_k)

        # 面积比
        mianji=round((z_k*z_g)/(f_k*f_g),3)
        print("mianji",mianji)

        if mianji>0.06:
            cv2.putText(img_hua,"smile",(int(wz[0]),int(wz[1])),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        else:
            cv2.putText(img_hua,"no-smile",(int(wz[0]),int(wz[1])),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.imshow("hua",img_hua)
    else:
        print('no_face')
        

# img_1=cv2.imread("C:/Users/29870/PycharmProjects/pinganchengshi/yichang/tupian/img.png")
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS,10)
if cap.isOpened():
    key=True
else:
    key=False
while key:
    key,image1=cap.read()
    image=cv2.resize(image1,(512,384))
    jiance(image)
    # cv2.imshow("image",image)
    if cv2.waitKey(1)&0xff==ord('q'):
        break
