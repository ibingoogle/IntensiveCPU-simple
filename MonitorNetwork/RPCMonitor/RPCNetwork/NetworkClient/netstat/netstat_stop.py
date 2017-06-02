#!/bin/python
# each Iftop instance is an RPC client
# the client keeps monitoring the network and reporting the result to RPC server at self.interval frequency

import subprocess
import sys

try:
	cur_path = sys.path[0]
	file = open(cur_path + "/iftop_pid", "r")
	pid = file.readline()
except (IOError, OSError) as error:
	print("error during iftop_pid file loading %s", error)
	file.close()

print(pid)
command = "kill -s 9 " + str(pid)
val = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
val.wait()
