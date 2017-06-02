#!/bin/python
import sys
import os
import socket
import subprocess

class Stop:

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

	def stop(self):
		self.stop_slaves()
		self.stop_master()


	def stop_master(self):
		command = "python " + self.cur_path + "/NetworkServer/NetworkMonitor_stop.py"
		#print(command)
		val = subprocess.Popen(command, shell=True)

	def stop_slaves(self):
		for slave in self.slaves:
			self.deploy_slave = slave
			command = "ssh " + self.user_name + "@" + self.deploy_slave + " python " + self.client_abspath + "/" + self.monitor_name + "/" + self.client_name + "/" + self.monitor_type + "/" + self.monitor_type + "_stop.py 2>/dev/null"
			#print(command)
			val = subprocess.Popen(command, shell=True)

if __name__=="__main__":

	TheStop = Stop()

	TheStop.stop()
