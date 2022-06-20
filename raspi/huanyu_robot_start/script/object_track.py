#!/usr/bin/env python
#huanyuRobot 

import rospy
from geometry_msgs.msg import Twist
from darknet_ros_msgs.msg import BoundingBoxes 
 
class ObjectTrack:
  def __init__(self):
    self.image_sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, self.bounding_boxes_callback)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

 
  def bounding_boxes_callback(self, msg):
  	
    for bounding_box in msg.bounding_boxes:
        if bounding_box.Class == "person":
            print "probability=%s,xmin=%s,ymin=%s,xmax=%s,ymax=%s"%(bounding_box.probability, bounding_box.xmin, bounding_box.ymin, bounding_box.xmax, bounding_box.ymax)
    print "\n\r"
 


if __name__ == '__main__':
	rospy.init_node('objetc_track_node', anonymous=False)
	darknet_result = ObjectTrack()
	rospy.spin()