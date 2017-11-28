#!/usr/bin/env python

import rospy
import roslib
import actionlib
from pa.msg import *

class TurnAction(object):
	_feedback = pa.msg.turn_cmdFeedback()
	_result = pa.msg.turn_cmdResult()

	def __init__(self, name):
		self.action_name = name
		self._as = actionlib.SimpleActionServer(self.action_name, pa.msg.turn_cmdAction, execute_cb=self.execute_cb, auto_start=False)
		self._as.start()

	def execute_cb(self, goal):
		r = rospy.Rate(1)
		success = True
		rospy.loginfo('Executing action')
		rospy.loginfo(goal.angle)
		rad = abs(goal.angle * 3.14/180)
		rospy.loginfo(rad)
		i = 0.174533
		turned = 10
		self._feedback.current_turn_angle = 0
		while i < rad:
			if self._as.is_preempt_requested():
				rospy.loginfo('Preempted')
				self._as.set_preempted()
				success = False
				break
			if goal.angle > 0:
				self._feedback.current_turn_angle = i
			else:
				self._feedback.current_turn_angle = -i
			self._as.publish_feedback(self._feedback)
			i = i + 0.174533
			print("turned " + str(turned))
			turned = turned + 10
			r.sleep()
		if success:
			self._result.total_turn_angle = self._feedback.current_turn_angle
			self._as.set_succeeded(self._result)

if __name__ == '__main__':
    rospy.init_node('actionServer')
    server = TurnAction('cmd_action')
    rospy.spin()

		
