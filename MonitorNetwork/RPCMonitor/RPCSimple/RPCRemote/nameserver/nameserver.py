import Pyro4

# nameserver is used to map the proxy name to the class in RPC server 
# we can locate nameserver with RPC server (192.168.2.31)
# but in this example, we put it in another node (192.168.2.32)

Pyro4.naming.startNSloop(host='192.168.2.32')
