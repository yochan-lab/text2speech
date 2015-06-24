#! /usr/bin/env python

__author__ = 'daniel'

import roslib
roslib.load_manifest('my_pkg_name')
import rospy
import actionlib
from subprocess import call, Popen
from os import environ as env, remove, system

from text2speech.msg import speakAction

language = "en-US"
volume = "1.0"

class SpeakServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer('speak', SpeakAction, self.execute, False)
        server.start()

    def execute(self, goal):
        global language, volume
        rospy.loginfo(rospy.get_caller_id() + "I said %s", goal.data)
        temp = '/tmp/text2speech-' + env['USER'] + '.wav'
        command = ['pico2wave', '-w', temp, goal.data]
        try:
            call(command)
        except OSError:
            #TODO: add detailed error message
            self.server.set_aborted(self, False, "my bad")
            exit(1)

        command = ['play', "-q",
                   "-v", volume,
                   temp]
        #TODO: add more options
        system(" ".join(command))
        remove(temp)
        self.server.set_succeeded(self, True, "hello again")

if __name__ == '__main__':
    rospy.init_node('speak_server')
    server = SpeakServer()
    rospy.spin();