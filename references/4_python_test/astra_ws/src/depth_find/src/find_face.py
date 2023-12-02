#! /usr/bin/python
# coding=utf-8
import rospy
import cv2
import numpy as np
import message_filters
import dlib
# 导入正则表达式模块
import re
#倒入自定义的数据类型
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
from depth_find.msg import shan

cv2.namedWindow('depth',cv2.WINDOW_NORMAL)

# 正向人脸检测
detector = dlib.get_frontal_face_detector()


# 用于处理检测到人脸的第一帧并确定待追踪人脸
def first_to_renlian(img1):

    #  灰度转换
    huidu = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    #  调用dlib库中的检测器
    detector = dlib.get_frontal_face_detector()
    # 检测人脸
    faces = detector(huidu, 1)  # 1 ：代表将图片放大一倍
    result=[]
    face_xiangliang=[]
    nofaces=[]
    if len(faces) ==1:
        print("检测到" + str(len(faces)) + "人")
        for face in faces:
            # 转换字符串
            string = str(face)
            # 提取数字，即人脸的位置信息
            position = re.findall(r"\d+", string)
            # 保存坐标
            for i in range(4):
                result.append(int(position[i]))
        centor_x=int(result[0]-((result[0]-result[2])*0.5))
        centor_y=int(result[1]-((result[1]-result[3])*0.5))
        return int(centor_x/4),int(centor_y/4)
    else:
        print('no_face')
        return 0,0

def callback(data1,data2):
    ap=0.0637
    #if Image.encoding is None:
        #print('none')
    #else:
        #print(Image.encoding)
    bridge = CvBridge()
    depth_image = bridge.imgmsg_to_cv2(data1, "16UC1")
    color_image = bridge.imgmsg_to_cv2(data2, "bgr8")
    #print(depth_image.shape,color_image.shape)
    x,y=first_to_renlian(color_image)
    x=int(x/4)
    y=int(y/4)
    #print(x,y)
    depth_1=cv2.applyColorMap(cv2.convertScaleAbs(depth_image,alpha=ap),cv2.COLORMAP_JET)
    if x+y==0:
        pass
    else:
        face_long=(depth_image[x,y]/ap)/1000
        fabu(round(face_long,2))
    #cv2.imshow('depth',depth_1)
    #cv2.waitKey(10)
    

def fabu(c):
    pub=rospy.Publisher('long',shan,queue_size=1)
    rate=rospy.Rate(1)
    rospy.loginfo('the face long is : '+str(c))
    pub.publish(shan(c))
    rate.sleep

def listener():
    rospy.init_node('pylistener', anonymous=True)
    
    depth=message_filters.Subscriber('/camera/depth/image_raw',Image)
    color=message_filters.Subscriber('/camera/color/image_raw',Image)
    color_depth=message_filters.ApproximateTimeSynchronizer([depth,color],10,1,allow_headerless=True)
    color_depth.registerCallback(callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
    
    


