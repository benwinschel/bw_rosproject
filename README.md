# bw_rosproject
Ben Winschel ROS Programming Assignment

# Instructions to Run:
Go into your __catkin_ws__ and run ```catkin_create_pkg pa rospy```. Download the source code and place the contents of the pa folder into the src subfolder of your pa package in your __catkin_ws__. Then run ```catkin_make``` and then ```roslaunch pa pa.launch```. Commands such as _turn 45_ are acceptable. If no angle is supplied, an error will be thrown. Can be run with Gazebo to illustrate performance.

# Key Ideas:
The consoleNode simply captures raw input from the terminal and publishes it to a ROS topic. An interesting problem I had was that when I tried to shutdown, the main node would block, waiting for console input, so it would never terminate gracefully. I had to include ```signal.signal(signal.SIGINT, handler)``` so that it would capture the termination command and use the exit handler to exit gracefully.

In the mainNode's callback for the published turn angle, I wait for the service and then send the published data. The service just applies a regex to the data, extracting the turn angle, (both positive and negative), and returns that back to the __degs__ variable in the mainNode. I then start a client to the actionServer, and send a goal with the angle returned by the service. This submission to the actionServer triggers two separate callbacks, the __feedback__ and __result__ callbacks. The actionServer publishes a feedback message once every second, saying the TB3 has turned 10 degrees. Therefore, in the callback, I match the speed and magnitude of the actionServer by publishing a Twist message once every second with an angular value of 10 degrees, causing the TB3 to turn 10 degrees every second.

In the __result__ feedback, I caluclate how much left I have to turn, which is an angle value between 1 and 9, and then set a Twist message's angular spped to be that value and publish it for one second, causing the TB3 to turn the remaining degrees.

The mainNode then returns to the original consoleNode callback and publishes an empty Twist message, causing the TB3 to stop turning.

Essentially we have this information flow:

![alt text](https://github.com/campusrover/bw_rosproject/blob/master/Drawing%20(10).png)

The mainNode is responsible for handling the callbacks for the actionServer, the service call, and the message publishing & subscribing.
