tmux new -d -s roscore 'roscore'
sleep 5
echo "started roscore"
tmux new -d -s frontCam 'roslaunch freenect_launch freenect.launch depth_registration:=true camera:=frontCamera device_id:=#1'
sleep 3
echo "started frontCam"
#tmux new -d -s rearCam 'roslaunch freenect_launch freenect.launch camera:=rearCamera device_id:=#2'
#sleep 3
echo "done with cameras"

#tmux new -d -s rearScanner 'export ROS_NAMESPACE=/rearScanner; \
#rosrun pointcloud_to_laserscan pointcloud_to_laserscan_node \
#	cloud_in:=/rearCamera/depth_registered/points \
#	_range_min:=0.1 \
#	_range_max:=30 \
#	_target_frame:=rearCamera_link'

#this runs the laser scanner and transforms it so it matches the point cloud
tmux new -d -s frontScanner 'export ROS_NAMESPACE=/frontScanner; \
rosrun pointcloud_to_laserscan pointcloud_to_laserscan_node \
	cloud_in:=/frontCamera/depth_registered/points \
	_range_min:=0.1 \
	_range_max:=10 \
	_target_frame:=frontCamera_link \
	_angle_min:=-0.50 \
	_angle_max:=0.50 \
	_use_inf:=false'


#echo "all done"
