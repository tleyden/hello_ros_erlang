
roscore &

epmd -daemon &

rosrun turtlesim turtlesim_node &

# this is wrong.. TODO: an erlang node that runs in the background and prints what it receives
erl -sname enode1@localhost -setcookie cookie &

echo "waiting for other stuff to startup  .."
sleep 5

echo "running python script .."
./hello_ros_erlang.py