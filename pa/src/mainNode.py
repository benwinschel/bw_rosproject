#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from pa.srv import cmd
import actionlib
import pa.msg
from geometry_msgs.msg import Twist
from actionlib_msgs.msg import GoalStatusArray
from pa.msg import turn_cmdActionFeedback
from pa.msg import turn_cmdActionResult
import time

def cmd_callback(msg):
	global degs
	rospy.wait_for_service('turn')
	try:
		turn = rospy.ServiceProxy('turn', cmd)
		resp = turn(msg.data)
		degs = resp.rad
		print('Successfully retrieved angle!')
		client = actionlib.SimpleActionClient('cmd_action', pa.msg.turn_cmdAction)
		client.wait_for_server()
		goal = pa.msg.turn_cmdGoal(angle=degs)
		client.send_goal(goal)
		client.wait_for_result()
		cmd_pub.publish(Twist())
		print("Command:")
	except rospy.ServiceException, e:
		print('Service Call Failed')

def feedback(msg):
	if msg.feedback.current_turn_angle != 0:
		twist = Twist()
		if msg.feedback.current_turn_angle > 0:
			twist.angular.z = 0.174533
		else:
			twist.angular.z = -0.174533	
		cmd_pub.publish(twist)
		rate.sleep()

def result(msg):
	print('Succeeded')
	print(msg)
	left_over = (degs * 3.14/180) - msg.result.total_turn_angle
	print(left_over)
	twist = Twist()
	twist.angular.z = left_over
	start_time = time.time()
	while time.time() - start_time <= 1:
		cmd_pub.publish(twist)
	

	

def main():
	global cmd_pub
	global rate
	cmd_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
	cmd_sub = rospy.Subscriber('/demo/command', String, cmd_callback)
	feedback_sub = rospy.Subscriber('/cmd_action/feedback', turn_cmdActionFeedback, feedback)
	result_sub = rospy.Subscriber('/cmd_action/result', turn_cmdActionResult, result)
	rospy.init_node('mainNode')
	rate = rospy.Rate(5)
	rospy.spin()


if __name__ == "__main__":
	main()
