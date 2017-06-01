#!/bin/Python

# warehouse.py is RPC server
# run warehoust.py is the remote node (192.168.2.31)
# the printed content is shown in the remote node


from __future__ import print_function
import Pyro4


# derived from object is the new feature of Python 3
@Pyro4.expose
class Warehouse(object):

	def __init__(self):
		self.contents = ["chair", "bike", "flashlight", "laptop", 'couch']

	def list_contents(self):
		return self.contents

	def take(self, name, item):
		self.contents.remove(item)
		print("{0} took the {1}.".format(name, item))

	def store(self, name, item):
		self.contents.append(item)
		print("{0} stored the {1}.".format(name, item))

def main():
	# locate the nameserver
	# Pyro4.naming.locateNS(host='192.168.2.32')
	# set the proxy name(example.warehouse) of the class Warehouse, also set the remote node ip
	# Pyro4.Daemon.serveSimple({Warehouse:"example.warehouse"}, ns=True, host='192.168.2.31')

	# set the remote node ip
	daemon = Pyro4.Daemon(host='192.168.2.31')
	# put the nameserver with RPC server
	ns	   = Pyro4.locateNS()
	# register the class in RPC server
	uri    = daemon.register(Warehouse)
	# register the class's proxy name in the nameserver
	ns.register("warehouse", uri)
	daemon.requestLoop()
	
	
if __name__=="__main__":
	main()
