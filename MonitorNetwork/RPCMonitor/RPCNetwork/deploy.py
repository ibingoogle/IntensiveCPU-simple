#!/bin/python
import sys
import os
import socket

class Deploy:

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

	def deploy(self):
		for slave in self.slaves:
			self.deploy_slave = slave
			print(self.deploy_slave)
			# miss some command if executing refresh() and copy() at the same time
			# so please pre refresh the dir in slaves and then do the copy 
			#self.refresh()
			self.copy()

	def refresh(self):
		command_monitor = "ssh " + self.user_name + "@" + self.deploy_slave + " mkdir " + self.client_abspath + "/" + self.monitor_name + " 2>/dev/null"
		os.popen(command_monitor)
		command_client = "ssh " + self.user_name + "@" + self.deploy_slave + " rm -rf " + self.client_abspath + "/" + self.monitor_name + "/" + self.client_name + " 2>/dev/null"
		os.popen(command_client)

	def copy(self):
		command_copy = "scp -r " + self.cur_path + "/" + self.client_name + " " + self.user_name + "@" + self.deploy_slave + ":" + self.client_abspath + "/" + self.monitor_name
		os.popen(command_copy)


if __name__=="__main__":

	TheDeploy = Deploy()

	TheDeploy.deploy()
