#!/usr/bin/env python

## Reads turtle coordinates from a ros topic and forwards to an erlang node
## See README.md for more details

import sys, getopt, types
  
PKG = 'hello_ros_erlang' # this package name
import roslib; roslib.load_manifest(PKG)
import rospy
from std_msgs.msg import String
from turtlesim.msg import Pose
from turtlesim.msg import Velocity

from py_interface import erl_node, erl_opts, erl_eventhandler, erl_term

ERLANG_REMOTE_NODE_REGISTERED_PROCESS = 'enode1_process'
ERLANG_REMOTE_NODE_NAME = 'enode1@localhost'
SELF_NODE_NAME = "hello_ros_erlang_node@localhost"
ERLANG_COOKIE = "hello_ros_erlang_cookie"
SELF_NODE_REGISTERED_PROCESS = "hello_ros_erlang_mailbox"
ROS_NODE_NAME = 'hello_ros_erlang'
ROS_TOPIC_POSE = "/turtle1/pose"
ROS_TOPIC_COMMAND_VELOCITY = "/turtle1/command_velocity"
VERBOSE = True

def ros_receive_topic_message(data):
    if VERBOSE:
        rospy.loginfo("Ros topic messsage " + rospy.get_caller_id() + " x: %s y: %s", data.x, data.y)
    send_turtle_pose_erlang(data)

def erlang_node_receive_message(msg, *k, **kw):
    global evhand
    if VERBOSE:
        print "Incoming msg=%s (k=%s, kw=%s)" % (`msg`, `k`, `kw`)
    msg_type = msg[1]
    if str(msg_type) == "stop":
        print "Exiting"
        evhand.StopLooping()
    elif str(msg_type) == "command_velocity":
        global publisher_command_velocity
        velocity_tuple = msg[2]
        # velocity = Velocity(velocity_tuple)
        if VERBOSE:
            print "Moving the turtle"
        publisher_command_velocity.publish(velocity_tuple[0], velocity_tuple[1])
        

def send_turtle_pose_erlang(data):
    global mailbox
    node_name_atom = erl_term.ErlAtom(ERLANG_REMOTE_NODE_NAME)
    remote_pid = erl_term.ErlPid(node=node_name_atom, id=38, serial=0, creation=1)
    msg_data = erl_term.ErlNumber(data.x)
    self_node_name = erl_term.ErlAtom("%s" % SELF_NODE_NAME)
    self_reg_process = erl_term.ErlAtom("%s" % SELF_NODE_REGISTERED_PROCESS)
    return_addr = erl_term.ErlTuple([self_node_name, self_reg_process])
    msg = erl_term.ErlTuple([return_addr, msg_data])
    remote_process_atom = erl_term.ErlAtom("%s" % ERLANG_REMOTE_NODE_REGISTERED_PROCESS)
    dest = erl_term.ErlTuple([remote_process_atom, node_name_atom])
    mailbox.Send(dest, msg)
    if VERBOSE:
        print "Sent message to (%s,%s)" % (ERLANG_REMOTE_NODE_REGISTERED_PROCESS, ERLANG_REMOTE_NODE_NAME)

def init_erlang_node():
    node = erl_node.ErlNode(SELF_NODE_NAME, erl_opts.ErlNodeOpts(cookie=ERLANG_COOKIE))
    node.Publish()
    return node

def init_erlang_mailbox(node):
    global mailbox
    mailbox = node.CreateMBox(erlang_node_receive_message)
    mailbox.RegisterName(SELF_NODE_REGISTERED_PROCESS)

def run_erlang_event_handler():
    global evhand
    evhand = erl_eventhandler.GetEventHandler()
    evhand.Loop()    

def init_ros():
    global publisher_command_velocity
    rospy.init_node(ROS_NODE_NAME, anonymous=True)
    rospy.Subscriber(ROS_TOPIC_POSE, Pose, ros_receive_topic_message)
    publisher_command_velocity = rospy.Publisher(ROS_TOPIC_COMMAND_VELOCITY, Velocity)

if __name__ == '__main__':
    init_ros()
    node = init_erlang_node()
    init_erlang_mailbox(node)
    run_erlang_event_handler() # blocks
