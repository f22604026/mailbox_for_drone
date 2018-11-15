#!/usr/bin/env python
# Hung-Chen Yu 11-10-2018 test
import rospy
import numpy as np
import math
import mavros_msgs
import time
import sys

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
    rospy.init_node('Offboard_waypoint_node', anonymous = True)
    rate = rospy.Rate(20) #publish at 20 Hz
    local_position_subscribe = rospy.Subscriber('/mavros/mocap/pose', PoseStamped, pos_sub_callback)



    while not rospy.is_shutdown():
        print("\n\n Please check the waypoints list: \n\n")
        print(np.matrix(waypoints))

        print("\n\n")
        input_command = raw_input("If you want to go to start the drone, Enter 'i' and fire the drone:")
        i_test = 'i'

        if input_command == i_test :
            goal_pose_update(0)
            #print(goal_pose)
            local_position_pub.publish(goal_pose)

            check=goal_checker(current_pose.pose.position, goal_pose.pose.position)

            try:
                while check == False:
                    time.sleep(0.1)
                    check=goal_checker(current_pose.pose.position, goal_pose.pose.position)
            except  KeyboardInterrupt:
                print("Program Terminated1")

            print("Drone is in position and ready to go.....\n\n")

            input_command_2 = raw_input("If you want to start the task, Enter 'i':")

            waypoint_idx=1
            #======================================
            # TASK START

            if input_command_2 == i_test:
                while waypoint_idx < waypoints.shape[0] :

                    #print(waypoints[waypoint_idx,0])
                    # checking signal to wait
                    if waypoints[waypoint_idx,0] > 100:
                        print("\n\nstay there for" + str(waypoints[waypoint_idx,1]) + '...\n\n')
                        time.sleep(waypoints[waypoint_idx,1])
                        waypoint_idx = waypoint_idx +1


                    print('\nwaypoint '+str(waypoint_idx))
                    print(np.matrix(waypoints[waypoint_idx,:]))

                    # GO TO NEXT WATPOINT by keyboard input
                    input_command_3 = raw_input("If you want to go to the waypoint, Enter 'i':")
                    if input_command_3 == i_test:

                        goal_pose_update(waypoint_idx)
                        #print('Got to publisher')
                        local_position_pub.publish(goal_pose)

                        check=goal_checker(current_pose.pose.position, goal_pose.pose.position)

                        try:
                            while check == False:
                                local_position_pub.publish(goal_pose)
                                time.sleep(0.1)
                                check=goal_checker(current_pose.pose.position, goal_pose.pose.position)
                        except  KeyboardInterrupt:
                            print("Program Terminated1")

                        waypoint_idx = waypoint_idx +1

                    # task abort 
                    else:
                        print("kill")
                        goal_pose.pose.position.x = -4.91
                        goal_pose.pose.position.y = -1.64
                        goal_pose.pose.position.z = 0.5
                        local_position_pub.publish(goal_pose)
                print("Drone has return.....\n\n")
                print("=====================================================\n\n")




if __name__ == '__main__':
    main()
