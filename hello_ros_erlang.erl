-module(hello_ros_erlang).

-export([start/0, stop/0]).

start() ->
    Pid = spawn(fun loop/0),
    register(enode1_process, Pid),
    net_kernel:connect('hello_ros_erlang_node@localhost').

stop() ->
    {hello_ros_erlang_mailbox,'hello_ros_erlang_node@localhost'} ! {self(), stop}.

loop() ->
    receive 
	_ ->
	    io:format("got message: ~n"),
	    loop()	     
    end.
