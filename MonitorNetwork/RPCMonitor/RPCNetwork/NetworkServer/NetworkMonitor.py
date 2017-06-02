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


class HttpServer(Thread):

	def __init__(self, mastermonitor):
		Thread.__init__(self)
		self.master_monitor = mastermonitor

		self.host = ""
		self.port = 80
		self.conf = "/conf"
		self.form = "xml"
		self.post_content = {'user':'swang','a':'1','b':'2'}
		self.load_conf()

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.sock.bind((self.host, self.port))
		self.sock.listen(1)

	def start(self):
		Thread.start(self)

	def run(self):
		index = 1
		#infinite loop
		while True:
			index = index + 1
			self.post_content = self.master_monitor.get_monitor()
			# get connected socket and address
			conn, addr = self.sock.accept()
			request = conn.recv(1024)
			request_str = str(request, encoding = "utf-8")

			print ('Connect by: ', addr)
			print ('Request_str is:\n', request_str)

			content = self.convert_content(self.post_content)
			print("content = ", content)
			conn.sendall(bytes(content, encoding='utf-8'))
			#close connection
			conn.close()

	def load_conf(self):
		cur_path = sys.path[0]
		try:
			file = open(cur_path + self.conf, "r")
			self.host = file.readline().split("=")[1].strip("\n")
			self.port = int(file.readline().split("=")[1].strip("\n"))
			self.form = file.readline().split("=")[1].strip("\n")
		except (IOError,OSError) as error:
			print("error during conf loading %s", error)
			file.close()

	def convert_content(self,post_content):
		if self.form == "json":
			converted_values = self.to_json(post_content)
			return converted_values
		converted_values = self.to_xml(post_content)
		return converted_values

	def to_json(self,Dict):
		jdata = json.dumps(Dict)
		return jdata

	def to_xml(self,Dict):
		root_Dict = {}
		root_Dict['root'] = Dict
		convertedxml = xmltodict.unparse(root_Dict);
		return convertedxml

class MasterMonitor(object):

	def __init__(self, cur_path):
		self.slaves = [] # use array to store the registered slaves
		self.monitor = {} # use dict to store the monitor result
		self.cluster_file = cur_path + "/cluster.txt"

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
	TheHttpServer = HttpServer(master_monitor)
	TheHttpServer.start()

	# since all RPC clients update the shared variable self.monitor, so we use instance mastermonitor in the RPC
	RPCServer(mastermonitor)
	print("RPCServer is running")


