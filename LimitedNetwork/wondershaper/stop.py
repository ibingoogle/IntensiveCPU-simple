from conf import Cluster1Conf
import os
import sys

theConf = Cluster1Conf()

start_command_middle = "sudo bash /home/hadoop0master/workspace/Shell/wondershaper/wondershaper/wondershaper "
start_command_post = "-c -a eth0"

for slave in theConf.slaves:
	start_command_prev = "ssh hadoop0master@" + slave + " "
	start_command = start_command_prev + start_command_middle + start_command_post
	print start_command
	os.popen(start_command)
