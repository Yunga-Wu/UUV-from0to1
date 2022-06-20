#!/usr/bin/env python
#coding=utf-8
import time
import logging
import subprocess

import rospy
import roslaunch

'''python roslaunch启动ROS节点控制'''

if __name__ == '__main__':

    basDir = "/home/huanyu/"
    logging.basicConfig(filename='/home/huanyu/Documents/robot_upstart.log',filemode="w",format="%(asctime)s %(name)s:%(levelname)s:%(message)s",datefmt="%d-%M-%Y %H:%M:%S",level=logging.INFO)
    logging.info("---------------huanyu_robot_upstart---------------------------")

    while True:                       
        time.sleep(3)
        try:
            if rospy.has_param('/run_id'): # error if rocore is not running
                print("find run_id!----------")
                logging.info("find run_id!---------- ")
                time.sleep(2)
                break
        except Exception as e:
            print('wait run_id except: ', e)

    try:
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        launch = roslaunch.parent.ROSLaunchParent(uuid, ["%srobot_ws/src/huanyu_robot_start/launch/robot_upstart.launch"%basDir])    
        launch.start()

        rospy.loginfo("roslaunch 启动成功！")
        logging.info("roslaunch 启动成功！")
        
        launch.spin() # 阻塞


    except Exception as e:
        print('roslaunch except: ', e)
        rospy.logfatal(e)
        launch.shutdown()
       
    finally:
        print('Nodes shutdown! ')
        logging.info("Nodes shutdown!")
      # After Ctrl+C, stop all nodes from running
        launch.shutdown()
