#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import Int16
# This script will listen for joystick button 5 being toggled and
# send zero speed messages to the mux to disable the follower until
# button 5 is pressed again.

class BehaviorSwitch(object):
    def __init__(self):
        self.running = False

    def callback(self, joy_msg):
        if joy_msg.buttons[5] == 1:
            self.running = not self.running

        rospy.loginfo(repr(joy_msg))

    def run(self):
        rospy.init_node('behavior_switch', anonymous=True)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        pub = rospy.Publisher('cmd_vel_mux/input/switch', Twist, queue_size=10)
        rospy.Subscriber('joy', Joy, self.callback)
        tilt_pub = rospy.Publisher('/set_tilt_degree', Int16 , queue_size=1)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            tilt_degree=Int16()
            tilt_degree.data=0
            tilt_pub.publish(tilt_degree)
            if self.running:
                empty_msg = Twist()
                pub.publish(empty_msg)
            rate.sleep()
        self.cmd_vel_pub.publish(Twist())

if __name__ == '__main__':
    try:
        behavior_switch = BehaviorSwitch()
        behavior_switch.run()
    except rospy.ROSInterruptException:
        pass
