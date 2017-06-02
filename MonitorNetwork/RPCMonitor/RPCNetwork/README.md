#RPCNetwork

Three components:

1.HttpServer based on socket. So the network status can be visited at browser side

2.Network status collection through RPC based on Pyro4 in Python. The slave node runs python file in NetworkClient dir and the master node runs files in NetworkServer dir. Meanwhile, the slave node updates the monitor information at the interval of 1 second(can be modified).

3.Network status monitor tools: There are two way to monitor the network: iftop and netstat. iftop is a better one. To use iftop, slave nodes should install iftop-1.0pre4.tar.gz before using it as the monitor tool. Meanwhile, current iftop only update outflow status.
