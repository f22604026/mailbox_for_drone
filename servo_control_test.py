#!/usr/bin/env python
# Hung-Chen Yu 11-10-2018 test
import rospy
import numpy as np
import math
import mavros_msgs
import time
import sys
import wiringpi


from geometry_msgs.msg import PoseStamped
from mavros_msgs import srv
from mavros_msgs.msg import State

goal_pose = PoseStamped()
current_pose = PoseStamped()
current_state = State()

local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 20)

waypoint_csv_file_name = 'waypoints.csv'
waypoints = np.genfromtxt(waypoint_csv_file_name, delimiter=',' ,skip_header=True)
#==============Position Goal Checker=========================
def goal_checker(current_pose, goal_pose):
    #calculate eucledian distance between the current position and goal position
    dist = math.sqrt((current_pose.x-goal_pose.x)**2+(current_pose.y-goal_pose.y)**2+(current_pose.z-goal_pose.z)**2)
    if dist < 0.15: #define the acceptable region (meter) for drone to switch to next waypoint
        return True
    else:
        return False


def goal_pose_update(index):
    global goal_pose
    goal_pose.pose.position.x = waypoints[index,0]
    goal_pose.pose.position.y = waypoints[index,1]
    goal_pose.pose.position.z = waypoints[index,2]

def pos_sub_callback(pose_sub_data):
    global current_pose
    current_pose = pose_sub_data
    local_position_pub.publish(goal_pose)

def main():
    # use 'GPIO naming'
    servo_pin =
    wiringpi.wiringPiSetupGpio()

    # set #18 to be a PWM output
    wiringpi.pinMode(servo_pin, wiringpi.GPIO.PWM_OUTPUT)

    # set the PWM mode to milliseconds stype
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

    # divide down clock
    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)

    delay_period = 0.01

    while True:
            for pulse in range(50, 250, 1):
                    wiringpi.pwmWrite(servo_pin, pulse)
                    time.sleep(delay_period)
            for pulse in range(250, 50, -1):
                    wiringpi.pwmWrite(servo_pin, pulse)
                    time.sleep(delay_period)


if __name__ == '__main__':
    main()
