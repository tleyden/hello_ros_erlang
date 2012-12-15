-module(hello_ros_erlang).
-export([start/0, stop/0]).

%% Receives turtle coordinates that were forwarded from a ros topic

start() ->
    Pid = spawn(fun loop/0),
    register(enode1_process, Pid),

    %% TODO: retry loop for connection, otherwise we won't receive any messages!
    net_kernel:connect('hello_ros_erlang_node@localhost').

stop() ->
    {hello_ros_erlang_mailbox,'hello_ros_erlang_node@localhost'} ! {self(), stop},
    enode1_process ! stop,
    unregister(enode1_process).

loop() ->
    receive 
	stop ->
	    io:format("Stopping loop~n");
	TurtleXPosition ->
	    TurtleXPositionString = io_lib:format("~.1f",[TurtleXPosition]),
	    io:format("Turtle X Pos: ~p~n", TurtleXPositionString),
	    loop()
    end.
