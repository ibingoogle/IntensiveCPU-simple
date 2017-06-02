#!/bin/python
# each Iftop instance is an RPC client
# the client keeps monitoring the network and reporting the result to RPC server at self.interval frequency

from threading import Thread
import time
import subprocess
import sys
import Pyro4
import socket
import os

class Iftop(Thread):

	def __init__(self, cur_path):
		Thread.__init__(self)
		# network command related parameters
		self.is_iftop = True # whether keep monitoring
		self.interval = 1
		self.command = "sudo iftop -t -s " + str(self.interval) + " -B"

		# cluster information
		self.cluster_file = cur_path + "/cluster.txt"
		self.cluster = []

		# the network flow information between other nodes in the cluster and current node
		self.content = [] # effective information extracted from the raw output of iftop command
		self.flow_send = {} # more detailed information from self.content
		self.flow_recv = {}

		# get hostname and ip through socket
		self.hostname = socket.getfqdn(socket.gethostname())
		self.ip = socket.gethostbyname(self.hostname)

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

	def start(self):
		self.is_iftop = True
		self.load_cluster()
		Thread.start(self)

	def run(self):
		i = 0
		mastermonitor = self.get_proxy()
		while self.is_iftop == True:
			# execute the command and control the output of the command
			val = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
			val.wait()
			# get the command output
			return_content = val.stdout.readlines()
			self.analysis_iftop(return_content)
			self.load_flow()
			# currently, we only update the flow_send in the RPC_server!!!!!!
			mastermonitor.update_monitor(self.hostname, self.flow_send)
			mastermonitor.print_monitor()
			print(i)
			i = i + 1
		

	def analysis_iftop(content_inlines):
		# analysis the output and extract the effective information			
		self.content = []
		Begin = False
		End	  = False
		for line in content_inlines:
			if End == True:
				break
			str_line = str(line, encoding="utf-8").split("\n")[0]
			if "---" in str_line:
				if Begin == True
					End = True
					Begin = False
				else:
					Begin = False
				continue
			if Begin == True:
				self.content.append(str_line) # add effective information into self.content


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


	# load more detailed information from self.content
	def load_flow(self):
		self.reset_flow()
		line_flag = -1
		prev_line = ""
		for line in self.content:
			line_flag = line_flag + 1
			if line_flag%2 == 0: # skip the line in even flag, but record it
				prev_line = line
				continue
			line_splitted = line.split()
			ForeignAddress = line_splitted[0] # the other node which communicate with current one
			# analysis two lines one-time if the address is in the cluster
			if self.belong_cluster(ForeignAddress) == True:
				Send = prev_line.split()[3]
				Recv = line_splitted[2]
				# convert the flow unit info KB
				Send_format = self.format_KB(Send)*2
				Recv_format = self.format_KB(Recv)*2
				# put the result into the dict
				self.flow_send[ForeignAddress] = Send_format
				self.flow_recv[ForeignAddress] = Recv_format

	def belong_cluster(self,address):
		if address in self.cluster:
			return True
		return False

	def reset_flow(self):
		for key in self.flow_send:
			self.flow_send[key] = 0
		for key in self.flow_recv:
			self.flow_recv[key] = 0

	def format_KB(self, origin):
		if "MB" in origin
			str_num = origin.split("MB")[0]
			return float(str_num)*1024
		elif "KB" in origin
			str_num = origin.split("KB")[0]
			return float(str_num)
		elif "B" in origin
			str_num = origin.split("B")[0]
			return float(str_num)/1024

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
		file = open(cur_path + "/iftop_pid", "w")
		file.write(str(process_id))
	except (IOError, OSError) as error:
		print("error during iftop_pid file loading %s", error)
	file.close()

if __name__=="__main__":
	cur_path = sys.path[0]
	record_pid(cur_path)

	TheIftop = Iftop(cur_path)
	TheIftop.register()
	TheIftop.start()
