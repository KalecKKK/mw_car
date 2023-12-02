#!/usr/bin/env python
#coding=utf-8
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

from sensor_msgs.msg import Image

#倒入自定义的数据类型
from learn_topic.msg import person


def talker():
    pub = rospy.Publisher('person_topic', person, queue_size=10)
    rospy.init_node('pytalker', anonymous=True)
    rate = rospy.Rate(1)
    name='allen'
    rospy.loginfo('Talker: this man named %s', name)
    i = 0
    h=0
    while not rospy.is_shutdown():
            pub.publish(person('allen',i,h))
            i = i+1
            h=i+i
            rate.sleep()

if __name__ == '__main__':
    talker()


