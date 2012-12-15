#!/usr/bin/env python

## This is a "hello world" for communicating from ROS<->Erlang, via Python
## 
## This python process subscribes to a ROS topic, and forwards whatever it
## receives to an Erlang node
  
PKG = 'rospy_tutorials' # this package name
import roslib; roslib.load_manifest(PKG)

import rospy
from std_msgs.msg import String
from turtlesim.msg import Pose

import sys
import getopt
import types

from py_interface import erl_node
from py_interface import erl_opts
from py_interface import erl_eventhandler
from py_interface import erl_term

def callback(data):
    global mailbox
    print("callback called")
    rospy.loginfo(rospy.get_caller_id()+"x: %s y: %s", data.x, data.y)
    node_name_atom = erl_term.ErlAtom('enode1@localhost')
    remote_pid = erl_term.ErlPid(node=node_name_atom, id=38, serial=0, creation=2)
    msg = erl_term.ErlAtom("%s" % (data.x))
    mailbox.Send(remote_pid, msg)
    print "Sent message to %s" % (remote_pid)
    
def erlang_timer_callback(*k, **kw):
    global mailbox
    print "Timer callback called"
    #node_name_atom = erl_term.ErlAtom('enode1@localhost')
    #remote_pid = erl_term.ErlPid(node=node_name_atom, id=38, serial=0, creation=2)
    #msg = erl_term.ErlAtom("testmsg")
    #m.Send(remote_pid, msg)
    #print "Sent message to %s" % (remote_pid)

def erlang_mailbox_message_callback(msg, *k, **kw):
    print "Incoming msg=%s (k=%s, kw=%s)" % (`msg`, `k`, `kw`)
    if type(msg) == types.TupleType:
        if len(msg) == 2:
            print "len is 2"
            if erl_term.IsErlPid(msg[0]):
                dest = msg[0]
                print "Dest: %s" % (dest,)


def start_erlang_node_loop():

    # note: erlang port mapper deamon (epmd) must be running

    global mailbox

    hostName = "localhost"
    ownNodeName = "py_interface_test"
    cookie = "cookie"

    print "Creating erlang node with name %s..." % ownNodeName
    n = erl_node.ErlNode(ownNodeName, erl_opts.ErlNodeOpts(cookie=cookie))
    n.Publish()
    mailbox = n.CreateMBox(erlang_mailbox_message_callback)
    mailbox.RegisterName("p")
    evhand = erl_eventhandler.GetEventHandler()

    evhand.AddTimerEvent(1, erlang_timer_callback)


    evhand.Loop()



def listener():

    # in ROS, nodes are unique named. If two nodes with the same
    # node are launched, the previous one is kicked off. The 
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'talker' node so that multiple talkers can
    # run simultaenously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/turtle1/pose", Pose, callback)

    start_erlang_node_loop()

    # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin()
        
if __name__ == '__main__':
    print("main called")
    listener()
