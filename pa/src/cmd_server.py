#!/usr/bin/env python

import rospy
from pa.srv import *
import re


def handle_cmd(req):
	reg = re.compile('(\\+|-)?\\d+')
	print('Extracting angle from: ' + req.cmd)
	if reg.search(req.cmd) is not None:
		return cmdResponse(float(reg.search(req.cmd).group()))
	else:
		return 'NO ANGLE'

def cmd_server():
	rospy.init_node('cmd_server')
	s = rospy.Service('turn', cmd, handle_cmd)
	print('Ready to Accept Command')
	rospy.spin()


if __name__ == "__main__":
	cmd_server()
