
## This is a "hello world" example for communicating from ROS<->Erlang.

- It uses Python as the "glue".  
- On the ros side, it uses rospy.  
- On the erlang side, it uses py-interface.

## How it works
 
This python process subscribes to a ROS topic, and forwards whatever it
receives to an Erlang node via py-interface

## Dependencies

- ros
- rospy (ships with ros)
- turtlesim (ships with ros)
- erlang
- py-interface (http://www.lysator.liu.se/~tab/erlang/py_interface/)

## Add directory to 

    export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/path/to/hello_ros_erlang

## Building

Nothing to build aside from dependencies (eg, ros)

## Running

Start roscore:

    roscore

Start the ros turtle sim:

    rosrun turtlesim turtlesim_node

Start the erlang port mapper daemon:

    epmd -daemon 

Start the python script:

    ./hello_ros_erlang.py

Start the erlang shell:

    erl -sname enode1@localhost -setcookie hello_ros_erlang_cookie -s hello_ros_erlang start

