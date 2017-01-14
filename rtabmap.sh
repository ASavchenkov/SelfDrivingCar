cameraSpace=/frontCamera
roslaunch rtabmap_ros rgbd_mapping.launch rtabmap_args:="--delete_db_on_start" \
frame_id:=frontCamera_link \
rgb_topic:=$cameraSpace/rgb/image_rect_color \
depth_registered_topic:=$cameraSpace/depth_registered/image_raw \
camera_info_topic:=$cameraSpace/rgb/camera_info
