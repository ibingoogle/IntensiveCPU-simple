#!/bin/python
# each netstat instance is an RPC client
# the client keeps monitoring the network and reporting the result to RPC server at self.interval frequency

from threading import Thread
import time
import subprocess
import sys
import Pyro4
import socket
import os


# two sub threads, one keep running netstat command, another keeps obtaining the latest netstat content
class NetStat(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.is_netstat = True
		self.command = "netstat -t"
		self.content = []
		self.interval = 0.5

	def start(self):
		self.is_netstat = True
		Thread.start(self)

	def run(self):
		while self.is_netstat == True:
			val = subprocess.Popen(self.command,shell=True,stdout=subprocess.PIPE)
			val.wait()
			self.content =  val.stdout.readlines()
			time.sleep(self.interval)


class Monitor(Thread):

	def __init__(self, cur_path):
		Thread.__init__(self)
		self.netstat = NetStat()
		# network command related parameters
		self.interval = 1
		self.is_monitor = True

		# cluster information
		self.cluster_file = cur_path + "/cluster.txt"
		# print(self.cluster_file)
		self.cluster = []

		# the network flow information between other nodes in the cluster and current node
		self.content = []
		self.flow_send = {}
		self.flow_recv = {}

		# get hostname and ip through socket
		self.hostname = socket.getfqdn(socket.gethostname())
		self.ip = socket.gethostbyname(self.hostname)

	def start(self):
		self.is_monitor = True
		self.load_cluster()
		self.netstat.start()
		Thread.start(self)

	def run(self):
		mastermonitor = self.get_proxy()
		while self.is_monitor == True:
			return_content =  self.netstat.content
			time.sleep(self.interval)
			self.analysis_netstat(return_content)
			self.load_flow()
			mastermonitor.update_monitor(self.hostname, self.flow_send)
			#mastermonitor.print_monitor()

	# get the class/instance from RPC server, register RPC client and print current information
	def register(self):
		mastermonitor = self.get_proxy()
		mastermonitor.add_slave(self.hostname)
		mastermonitor.print_slave()
		mastermonitor.print_monitor()

	# get the class/instance from RPC server
	def get_proxy(self):
		mastermonitor = Pyro4.Proxy("PYRONAME:MasterMonitor")
		return mastermonitor

	# figure out the nodes in the cluster we need monitor
	def load_cluster(self):
		# clean everything
		del self.cluster[:]
		self.flow_send.clear()
		self.flow_recv.clear()
		try:
			file = open(self.cluster_file, "r")
			lines = file.readlines()
			for line in lines:
				hostname = line.split("\n")[0]
				self.cluster.append(hostname)
				self.flow_send[hostname] = 0
				self.flow_recv[hostname] = 0
		except (IOError, OSError) as error:
			print("error during cluster_file loading %s", error)
			return False
		return True


	def analysis_netstat(self,content_inlines):
		del self.content[:]
		self.reset_flow()
		for line in content_inlines:
			#flow = line.split("\n")[0]
			#print(line)
			str_line = str(line, encoding="utf-8")
			#print(str_line)
			flow = str_line.split("\n")[0]
			flow_splited = flow.split()
			#print len(flow_splited)
			sub_flow = []
			if len(flow_splited) == 6:
				for split in flow_splited:
					sub_flow.append(split)
					self.content.append(sub_flow)
		print(self.content)


	# load more detailed information from self.content
	def load_flow(self):
		for sub_flow in self.content:
			ForeignAddressIp = sub_flow[4].split(":")[0]
			recv = sub_flow[1]
			send = sub_flow[2]
			if self.belong_cluster(ForeignAddressIp) == True:
				current_recv = self.flow_recv[ForeignAddressIp]
				current_send    = self.flow_send[ForeignAddressIp]
				self.flow_recv[ForeignAddressIp] = current_recv + int(recv)
				self.flow_send[ForeignAddressIp]    = current_send    + int(send)
		self.print_flow_send()
		self.print_flow_recv()

	def belong_cluster(self,address):
		if address in self.cluster:
			return True
		return False

	def reset_flow(self):
		for key in self.flow_send:
			self.flow_send[key] = 0
		for key in self.flow_recv:
			self.flow_recv[key] = 0


	def print_flow_send(self):
		print("flow_send_ssssssssssssssssssssssssss")
		for key in self.flow_send:
			print("hostname: ", key)
			print("send: ", self.flow_send[key])

	def print_flow_recv(self):
		print("flow_recv_rrrrrrrrrrrrrrrrrrrrrrrrrr")
		for key in self.flow_recv:
			print("hostname: ", key)
			print("send: ", self.flow_recv[key])


def record_pid(cur_path):
	process_id = os.getpid()
	try:
		file = open(cur_path + "/netstat_pid", "w")
		file.write(str(process_id))
	except (IOError, OSError) as error:
		print("error during netstat_pid file loading %s", error)
	file.close()

if __name__=="__main__":
	cur_path = sys.path[0]
	record_pid(cur_path)

	TheMonitor = Monitor(cur_path)
	TheMonitor.register()
	TheMonitor.start()
