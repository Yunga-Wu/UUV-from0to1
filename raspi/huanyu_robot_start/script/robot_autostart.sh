#!/bin/bash

source /opt/ros/melodic/setup.bash
source /home/huanyu/robot_ws/devel/setup.bash
export ROS_MASTER_URI=http://192.168.1.140:11311
export ROS_HOSTNAME=192.168.1.140

LOGPATH=/home/huanyu/Documents/autostart.log
echo '-------------start------------------------' >> $LOGPATH
echo `date` >> $LOGPATH
# Start roscore
roscore & >> $LOGPATH
sleep 2
echo "roslaunch begin ..." >> $LOGPATH

INDEX=0
RET=

RET=`ps -ef|grep -v grep|grep robot_upstart.py`
if [ "" == "$RET" ];then
    echo "robot_upstart.py is null, then start---" >> $LOGPATH 
	/usr/bin/python2.7 /home/huanyu/robot_ws/src/huanyu_robot_start/script/robot_upstart.py   >> $LOGPATH
else
	echo "robot_upstart.py is already started... " >> $LOGPATH
fi

echo "roslaunch end ..." >> $LOGPATH
echo `date` >> $LOGPATH



