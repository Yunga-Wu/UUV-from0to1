source /opt/ros/melodic/setup.bash
source /home/huanyu/robot_ws/devel/setup.bash
export ROS_MASTER_URI=http://192.168.1.140:11311
export ROS_HOSTNAME=192.168.1.140

LOGPATH=/home/huanyu/Documents/autostart_stop.log
echo '--------------stop-----------------------' >> $LOGPATH
echo `date` >> $LOGPATH

for i in $(rosnode list);do
    rosnode kill $i;
done
killall roslaunch
killall roscore
sleep 2
echo `date` >> $LOGPATH
echo 'stop end' >> $LOGPATH

exit 0 #执行完要结束进程
