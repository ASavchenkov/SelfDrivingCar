#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import time

from steamcontroller import SteamController
from steamcontroller.events import EventMapper, Pos

import threading
import serial

import math
import numpy as np

globalOdom = 0
#45 degrees is the center
globalSteering = 45
globalMoveCommand = 'n'
autonomous = False

autoSteerCommand = 'c'
autoDriveCommand = 'n'

def odomCallback(data):
    global globalOdom
    globalOdom = data

def scannerCallback(data):
    # print data
    global autoSteerCommand
    global autoDriveCommand
    scan = data.ranges
    averaged = [np.mean(scan[i:i+5]) for i in range(len(scan)-5)]
    worstDirection = np.argmin(averaged) 

    if(averaged[worstDirection]<3):
        autoSteerCommand = 'c'
        autoDriveCommand = 'n'
    elif(averaged[worstDirection]<5):
        if(worstDirection<len(averaged)/2): autoSteerCommand = 'l'
        else: autoSteerCommand = 'r'
        autoDriveCommand = 'f'
    else:
        autoSteerCommand = 'c'
        autoDriveCommand = 'f'
    
    print(autoSteerCommand,autoDriveCommand)


    

def int_to_bool_list(num):
    return [bool(num & (1<<n)) for n in range(32)]

def testSciCallback(_,sci):

    global globalSteering
    global globalMoveCommand
    global autonomous


    buttons =  int_to_bool_list(sci.buttons)
    
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
    print('this function is running')
    sc = SteamController(callback=testSciCallback)
    sc.run()
   

if __name__ == '__main__':
    
    scThread = threading.Thread(target=scFunc)
    scThread.setDaemon(True)
    scThread.start()

    rospy.init_node('robotController',anonymous=True)
    # rospy.Subscriber('/rtabmap/odom',Odometry, odomCallback)
    rospy.Subscriber('/frontScanner/scan',LaserScan,scannerCallback)
    rospy.loginfo('liked and subscribed!')
    

    curSteering = globalMoveCommand
    curMoveCommand = globalMoveCommand
    lastSteering = 45
    lastMoveCommand = 'n'

    # ser = serial.Serial('/dev/ttyACM0',9600)

    while(not rospy.is_shutdown()):
        lastSteering = curSteering
        lastMoveCommand = curMoveCommand
        curSteering = globalSteering
        curMoveCommand = globalMoveCommand
        # rospy.loginfo('mainloop %s, %f', globalMoveCommand,globalSteering)
        
        if(autonomous):
            
            pass
        command = curMoveCommand+str(curSteering)
        # ser.write(bytearray(command+ 'q','utf-8'))
         
        time.sleep(1.0/15.0)
        
