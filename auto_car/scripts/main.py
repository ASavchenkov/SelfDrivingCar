#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import time

from steamcontroller import SteamController
from steamcontroller.events import EventMapper, Pos

import threading

curOdomData = 0
#45 degrees is the center
curSteering = 0
curMoveCommand = 'n'

def odomCallback(data):
    global curOdomData
    curOdomData = data

def testSciCallback(_,sci):
    global curSteering
    global curMoveCommand

    curSteering = (float(sci.lpad_x)/32768+1)/2*90

    if (sci.rtrig>10 and sci.ltrig>10):
        if(sci.rtrig>sci.ltrig):curMoveCommand='f'
        else:curMoveCommand='r'
    elif(sci.rtrig>10): curMoveCommand = 'f'
    elif(sci.ltrig>10): curMoveCommand = 'r'
    else: curMoveCommand = 'n'
    

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
    while(not rospy.is_shutdown()):
        rospy.loginfo('mainloop %s, %f', curMoveCommand,curSteering)
        time.sleep(0.1)
