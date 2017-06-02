#!/bin/python
import sys
import os
import socket
import subprocess

class Monitor:

	monitor_type = "netstat"
	cur_path = ""
	client_abspath = "/home/hadoop0master/workspace/Python/RPC"
	monitor_name = "NetworkMonitor"
	client_name = "NetworkClient"
	user_name = "hadoop0master"
	
	slaves = []
	master = ""
	deploy_slave = "" #current deployed slave

	def __init__(self):
		self.cur_path = sys.path[0]
		print(self.cur_path)
		self.slaves = []
		self.master = socket.getfqdn(socket.gethostname())
		self.cluster_file = self.cur_path + "/cluster.txt"
		self.load_cluster()

	def load_cluster(self):
		try:
			file = open(self.cluster_file, "r")
			lines = file.readlines()
			for line in lines:
				line = line.split("\n")[0]
				if line != self.master:
					self.slaves.append(line)
		except (IOError,OSError) as error:
			print("error during cluster_file loading %s", error)

	def monitor(self):
		self.monitor_master()
		self.monitor_slaves()

	def monitor_master(self):
		command = "python " + self.cur_path + "/NetworkServer/NetworkMonitor.py"
		#print(command)
		val = subprocess.Popen(command, shell=True) # do not use os.popen(), we need sub thread

	def monitor_slaves(self):
		for slave in self.slaves:
			self.deploy_slave = slave
			command = "ssh " + self.user_name + "@" + self.deploy_slave + " python " + self.client_abspath + "/" + self.monitor_name + "/" + self.client_name + "/" + self.monitor_type + "/" + self.monitor_type + "_monitor.py"
			print(command)
			val = subprocess.Popen(command, shell=True) # do not use os.popen()

if __name__=="__main__":

	TheMonitor = Monitor()

	TheMonitor.monitor()
