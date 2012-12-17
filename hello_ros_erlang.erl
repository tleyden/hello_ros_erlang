-module(hello_ros_erlang).
-export([start/0, stop/0]).

%% Receives turtle coordinates that were forwarded from a ros topic

start() ->
    connect_to_remote_node().

stop() ->
    {hello_ros_erlang_mailbox,'hello_ros_erlang_node@localhost'} ! {self(), stop},
    enode1_process ! stop,
    unregister(enode1_process).

connect_to_remote_node() ->
    %% in order to be able to receive messages from hello_ros_erlang.py, we must connect
    ConnectedRemoteNode = net_kernel:connect('hello_ros_erlang_node@localhost'),
    case ConnectedRemoteNode of
	true ->
	    Pid = spawn(fun loop/0),
	    register(enode1_process, Pid);
	false ->
	    io:format("Could not connect to Python hello_ros_erlang_node, is it running? ~n")
    end.

move_turtle_randomly(SenderNodeName, SenderProcessName) ->
    {SenderProcessName, SenderNodeName} ! {self(), command_velocity, {2.0, 1.8}}.

loop() ->
    receive 
	stop ->
	    io:format("Stopping loop~n");
	TurtleMessage ->
	    { {SenderNodeName, SenderProcessName}, TurtleXPosition } = TurtleMessage,
	    io:format("Sender Node Name: ~p Process Name: ~p~n", [SenderNodeName, SenderProcessName]),
	    TurtleXPositionString = io_lib:format("~.1f",[TurtleXPosition]),
	    io:format("Turtle X Pos: ~p~n", TurtleXPositionString),
	    move_turtle_randomly(SenderNodeName, SenderProcessName),
	    loop()
    end.
