#! /usr/bin/python
# coding=utf-8
import rospy
import cv2
import numpy as np
import message_filters
#倒入自定义的数据类型
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
from depth_find.msg import shan

cv2.namedWindow('depth',cv2.WINDOW_NORMAL)

def chuli(img1):
    # 一米图优先级高，判断是否要转向
    # 一米图判断后，如果需要转向，则组织四米图运行
    # 一米图判断不需要转向，则四米图开始直行
    # 宽度设置为50-110
    # 高度为图像高度
    # 累计值num
    num=0
    for i in range(50,110):
        for j in range(img1.shape[0]):
            num=num+img1[j][i][2]
    num_jun=int(num/(60*120))
    #print(num_jun)
    return num_jun



def callback(data1,data2):

    #if Image.encoding is None:
        #print('none')
    #else:
        #print(Image.encoding)
    bridge = CvBridge()
    depth_image = bridge.imgmsg_to_cv2(data1, "16UC1")
    color_image = bridge.imgmsg_to_cv2(data2, "bgr8")
    
    #print(color_image.shape)
    #print(depth_image.shape)
    # 一米图,判断转向，优先级高
    dep_1=cv2.applyColorMap(cv2.convertScaleAbs(depth_image,alpha=0.3),cv2.COLORMAP_JET)
    chuli_image=chuli(dep_1)
    shan=0
    if chuli_image<100:
        a=0
        cv2.arrowedLine(color_image, (273, 420), (200, 420), (0, 255, 255), 30)
        cv2.arrowedLine(color_image, (367, 420), (440, 420), (0, 255, 255), 30)
        cv2.circle(color_image,(50,50),20,(0,0,0),-1)
        cv2.circle(color_image,(100,50),20,(0,0,255),-1)
    else: 
        
        cv2.line(color_image, (320, int(480 - (shan * 10))), (320, int(480 - (shan * 10 + 10))),
                         (255, 255, 255), 20)

        cv2.line(color_image, (320, int(480-40 - (shan * 10))), (320, int(480-40 - (shan * 10 + 10))),
                         (255, 255, 255), 20)

        cv2.line(color_image, (320, int(480-80 - (shan * 10))), (320, int(480-80 - (shan * 10 + 10))),
                         (255, 255, 255), 20)

        cv2.line(color_image, (320, int(480-120 - (shan * 10))), (320, int(480-120 - (shan * 10 + 10))),
                         (255, 255, 255), 20)

        cv2.line(color_image, (320, int(480-160 - (shan * 10))), (320, int(480-160 - (shan * 10 + 10))),
                         (255, 255, 255), 20)

        cv2.line(color_image, (320, int(480-200 - (shan * 10))), (320, int(480-200 - (shan * 10 + 10))),
                         (255, 255, 255), 20)
    
        cv2.circle(color_image,(50,50),20,(0,255,0),-1)
        cv2.circle(color_image,(100,50),20,(0,0,0),-1)



        #cv2.line(color_image, (320 - 40, int(480 - (shan * 10))), (320 - 40, int(480 - (shan * 10 + 10))),
                         #(255, 255, 255), 20)
        #cv2.line(color_image, (320 + 40, int(480 - (shan * 10))), (320 + 40, int(480 - (shan * 10 + 10))),
                         #(0, 255, 255), 20)

        cv2.line(color_image, (253-10, 480), (273, 240), (255, 255, 255), 2)
        cv2.line(color_image, (387+10, 480), (367, 240), (255, 255, 255), 2)
        a=1
    
        
    # 四米图，判断直行，优先级低
    #dep_4=cv2.applyColorMap(cv2.convertScaleAbs(depth_image,alpha=0.1),cv2.COLORMAP_JET)
    cv2.imshow('depth',dep_1)
    cv2.imshow('color',color_image)
    cv2.waitKey(10) 
    if a is None:
        pass 
    else:
        fabu(a)
        
    
def fabu(c):
    pub=rospy.Publisher('left_right',shan,queue_size=10)
    rate=rospy.Rate(10)
    if c==1:
        rospy.loginfo('It is a way. '+str(c))
    if c==0:
        rospy.loginfo('It is not a way. '+str(c))
    pub.publish(shan(c))
    rate.sleep

def listener():
    rospy.init_node('pylistener', anonymous=True)
    
    depth=message_filters.Subscriber('/camera/depth/image_raw',Image)
    color=message_filters.Subscriber('/camera/rgb/image_raw',Image)
    color_depth=message_filters.ApproximateTimeSynchronizer([depth,color],10,1,allow_headerless=True)
    color_depth.registerCallback(callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
    
    


