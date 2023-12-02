#!/usr/bin/env python
#coding=utf-8
import rospy
import cv2
#倒入自定义的数据类型
from learn_topic.msg import person


def callback(person):
    rospy.loginfo('Listener: %s''s age is %d and hight is %d', person.name, person.age,person.hight)

def listener():
    rospy.init_node('pylistener', anonymous=True)
    rospy.Subscriber('person_topic', person, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
    


