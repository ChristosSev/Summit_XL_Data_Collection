#!/usr/bin/env python

import rospy
import message_filters
import rosbag

from sensor_msgs.msg import Image
from sensor_msgs.msg import JointState
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud2
from tf2_msgs.msg import TFMessage

from datetime import date
from datetime import datetime

path = '/media/sneh/Heracleia/Robot_Data/Indoor_Data/Data-'


def callback(image, joints, front_laser,rear_laser, cloud):
    global bag

    bag.write('img', image)
    bag.write('joints', joints)
    bag.write('front_laser', front_laser)
    bag.write('rear_laser', rear_laser)
    bag.write('cloud', cloud)


global bag

if __name__ == '__main__':

    while not rospy.is_shutdown():

        today = date.today()
        now = datetime.now()

        time = now.strftime("%H-%M-%S")
        day = today.strftime("%m-%d-%y")

        rospy.init_node('data_recording')

        bag = rosbag.Bag(path + day+'-Time-' + time + '.bag', 'w')

        img_sub = message_filters.Subscriber('/robot/front_rgbd_camera/rgb/image_raw', Image)
        joint_sub = message_filters.Subscriber('/robot/joint_states', JointState)
        front_laser_sub = message_filters.Subscriber('/robot/front_laser/filtered_scan', LaserScan)
        rear_laser_sub = message_filters.Subscriber('/robot/rear_laser/filtered_scan', LaserScan)
        cloud_sub = message_filters.Subscriber('/robot/front_rgbd_camera/depth/points', PointCloud2)

        ts = message_filters.ApproximateTimeSynchronizer([img_sub, joint_sub, front_laser_sub, rear_laser_sub, cloud_sub], 10, 1, allow_headerless=False)
        ts.registerCallback(callback)

        rospy.spin()

    bag.close()

