#!/usr/bin/env python
__author__ = 'daniel'
#the real author is Kyle, most of this code is from his "picospeaker"

import rospy
import roslib
roslib.load_manifest('text2speech')
from std_msgs.msg import String

from subprocess import call, Popen
from os import environ as env, remove, system
from time import sleep

language = "en-US"
volume = "1.0"

def say(data):
    global language, volume
    rospy.loginfo(rospy.get_caller_id() + "I said %s", data.data)
    temp = '/tmp/text2speech-' + env['USER'] + '.wav'
    command = ['pico2wave', '-w', temp, data.data]
    try:
        call(command)
    except OSError:
        #TODO: add error message
        exit(1)

    command = ['play', "-q",
               "-v", volume,
               temp]
    #TODO: add more options
    system(" ".join(command))
    remove(temp)

def listener():
    global language, volume
    #language = rospy.get_param("~language", "en-US")
    #volume = rospy.get_param("~volume", 1.0)

    rospy.Subscriber("tosay", String, say,queue_size=1)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('text2speech')
    listener()
