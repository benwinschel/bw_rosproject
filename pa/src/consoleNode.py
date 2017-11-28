#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from threading import Thread
import sys
import signal

def handler(signal, frame):
	sys.exit(0)

rospy.init_node('consoleNode')
cmd_pub = rospy.Publisher('/demo/command', String, queue_size=1)
print('Command:')
while not rospy.is_shutdown():
	angle = raw_input()
	cmd_pub.publish(angle)
	signal.signal(signal.SIGINT, handler)

