# time-server-client
A simple multi-threaded time server and client in Python.

This uses the latest match/case command found in Python 3.10 so requires 3.10 version at minimum.
The time server can handle multiple clients and has the ability to shut down all threads 
gracefully after a KeyboardInterrupt exception is thrown. The client is also quite basic,
and both server and client has some network error handling.
