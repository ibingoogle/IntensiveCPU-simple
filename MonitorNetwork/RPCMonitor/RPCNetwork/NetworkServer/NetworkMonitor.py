#!/bin/python
# class HttpServer is the http server based on socket
# class MasterMonitor is the RPC server based on Pyro4
from __future__ import print_function
import Pyro4
import socket
import os
import sys
from threading import Thread
import threading
import re
import json
import xmltodict

# the lock is used when multiple clients request the server
mutex = threading.Lock()

class MasterMonitor(object):

	def __init__(self, cur_path):
		self.slaves = [] # use array to store the registered slaves
		self.monitor = {} # use dict to store the monitor result
		self.cluster_file = cur_path + "/cluster.txt"
		# self.load_cluster()

	def load_cluster(self):
		try:
			file = open(self.cluster_file, "r")
			lines = file.readlines()
			for line in lines:
				hostname = line.split("\n")[0]
				self.monitor[hostname] = 0 # initialize the monitor result as zero
		except (IOError,OSError) as error:
			print("error during cluster_file loading %s", error)

	def add_slave(self, slave):
		if slave in self.slaves:
			return
		self.slaves.append(slave)
		self.monitor[slave] = {} # initialize the monitor result of each slave as dict

	def update_monitor(self, slave, result): # update the result using lock
		mutex.acquire()
		self.monitor[slave] = result
		mutex.release()

	def get_monitor(self):
		return self.monitor

	def print_slave(self):
		for slave in self.slaves:
			print("slave = ", slave)

	def print_monitor(self, slave=None):
		if slave: # if specified
			print("monitor[", slave, "] = ", self.monitor[slave])
			return
		print("printall")
		print(self.monitor)
		return


# register the class MasterMonitor in the RPC
class RPCServerThread(Thread):

	def __init__(self):
		Thread.__init__(self)

	def start(self):
		Thread.start(self)

	def run(self):
		daemon = Pyro4.Daemon(host='192.168.2.30')
		ns	   = Pyro4.locateNS()
		uri	   = daemon.register(MasterMonitor)
		ns.register("MasterMonitor", uri)
		daemon.requestLoop()


# register the instance mastermonitor in the RPC
def RPCServer(mastermonitor):

	daemon = Pyro4.Daemon(host='192.168.2.30')
	ns	   = Pyro4.locateNS()
	uri	   = daemon.register(mastermonitor)
	ns.register("MasterMonitor", uri)
	daemon.requestLoop()

def record_pid(cur_path):
	process_id = os.getpid()
	try:
		file = open(cur_path + "/NetworkMonitor_pid", "w")
		file.write(str(process_id))
	except (IOError, OSError) as error:
		print("error during NetworkMonitor_pid file loading %s", error)
	file.close()


if __name__=="__main__":
	cur_path = sys.path[0]
	record_pid(cur_path)

	mastermonitor = MasterMonitor(cur_path)

	# since all RPC clients update the shared variable self.monitor, so we use instance mastermonitor in the RPC
	RPCServer(mastermonitor)
	print("RPCServer is running")


