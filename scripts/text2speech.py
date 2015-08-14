#!/usr/bin/env python
__author__ = 'daniel'
#the real author is Kyle, most of this code is from his "picospeaker"

import rospy
import roslib
roslib.load_manifest('text2speech')
from std_msgs.msg import String, Bool

from subprocess import call, Popen
from tempfile import NamedTemporaryFile
from os import environ as env, remove, system
from time import sleep

language = "en-US"
volume = "0.25"
pub = None

def say(words):
    pub.publish(True)
    rospy.loginfo(rospy.get_caller_id() + "I said %s", words)
    # temp = '/tmp/text2speech-' + env['USER'] + '.wav'
    temp = NamedTemporaryFile('w+b', suffix='.wav')
    command = ['pico2wave', '-w', temp.name, words]
    try:
        call(command)
    except OSError:
        #TODO: add error message
        pub.publish(False)
	return False

    command = ['play', "-q",
               "-v", volume,
               temp.name]
    #TODO: add more options
    system(" ".join(command))
    # remove(temp)
    temp.close()
    pub.publish(False)
    return True

class JoinableQueue(Queue):
    def __init__(self, maxsize=0):
	super(self, JoinableQueue).__init__(maxsize)
	self.next_task_done = _threading.Condition(self.mutex)

    def task_done(self, item):
        self.next_task_done.acquire()
        try:
	    self.next_task_done.notify_all()
        finally:
            self.next_task_done.release()
	    super(self, JoinableQueue).task_done()

    def join(self, item=None):
	if item is None:
	    return super(self, JoinableQueue).join()
        self.next_task_done.acquire()
        try:
	    while self._check(item):
                self.next_task_done.wait()
        finally:
            self.next_task_done.release()

    def _check(self, other):
	return other in self.queue

def say_as_service(req):
    return say(req.text)

def say_non_block(data):
    return say(data.data)

def listener():
    global language, volume, pub
    #language = rospy.get_param("~language", "en-US")
    #volume = rospy.get_param("~volume", 1.0)

    rospy.Subscriber("tosay", String, say, queue_size=1)
    pub = rospy.Publisher("is_speaking", Bool, queue_size=1)
    srv = rospy.Service('speak', Speak, say_as_service)
    pub.publish(False)
    rospy.spin()

word_queue = JoinableQueue()
if __name__ == '__main__':
    rospy.init_node('text2speech')
    listener()
