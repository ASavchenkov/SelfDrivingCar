#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import time

from steamcontroller import SteamController
from steamcontroller.events import EventMapper, Pos

import threading
import serial

import math

globalOdom = 0
#45 degrees is the center
globalSteering = 45
globalMoveCommand = 'n'
autonomous = False
ser = serial.Serial('/dev/ttyACM0',9600)

def odomCallback(data):
    global globalOdom
    globalOdom = data


def int_to_bool_list(num):
    return [bool(num & (1<<n)) for n in range(32)]

def testSciCallback(_,sci):

    global globalSteering
    global globalMoveCommand
    global autonomous
    # global ser
    # print(ser.readline().decode('ascii','replace'))


    buttons =  int_to_bool_list(sci.buttons)
    # print(zip(range(32),buttons))
    
    if(buttons[15]):autonomous = True
    else: autonomous = False
    globalSteering = int((float(sci.lpad_x)/32768)/2*90)
    if (sci.rtrig>10 and sci.ltrig>10):
        if(sci.rtrig>sci.ltrig):globalMoveCommand='f'
        else:globalMoveCommand='r'
    elif(sci.rtrig>10): globalMoveCommand = 'f'
    elif(sci.ltrig>10): globalMoveCommand = 'r'
    else: globalMoveCommand = 'n'
    

def scFunc():
    print('this function is runnig')
    sc = SteamController(callback=testSciCallback)
    sc.run()
   

if __name__ == '__main__':
    
    scThread = threading.Thread(target=scFunc)
    scThread.setDaemon(True)
    scThread.start()
    print('running the steam controller')
    rospy.init_node('robotController',anonymous=True)
    rospy.Subscriber('/rtabmap/odom',Odometry, odomCallback)
    rospy.loginfo('liked and subscribed!')
    

    curSteering = globalMoveCommand
    curMoveCommand = globalMoveCommand
    lastSteering = 45
    lastMoveCommand = 'n'

    waypoint =iter([[0,10],[0,0]]).next()

    while(not rospy.is_shutdown()):
        lastSteering = curSteering
        lastMoveCommand = curMoveCommand
        curSteering = globalSteering
        curMoveCommand = globalMoveCommand
        # rospy.loginfo('mainloop %s, %f', globalMoveCommand,globalSteering)
        
        if(autonomous):
            # print(globalOdom.pose.pose.position) 
            # print(globalOdom.pose.pose.orientation)
            # print(waypoint)
            pass
        # if(lastSteering!=curSteering or lastMoveCommand!=curMoveCommand):
        command = curMoveCommand+str(curSteering)
        ser.write(bytearray(command+ 'q','utf-8'))
         
        time.sleep(1.0/15.0)
        
