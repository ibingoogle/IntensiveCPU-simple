import os
import sys
import matplotlib.pyplot as plt
from Conf import Configuration


class FetchRemoteFiles:

	def __init__(self, hostname):
		self.scp_command_pre = "scp " + hostname + "@"
		self.scp_command_src = ":/opt/modules/bigdl-master-angelps/executioninfo/timefile_*"
		self.scp_command_dst = "/opt/modules/bigdl-master-angelps/executioninfo/"
		self.clear_command_pre = "ssh " + hostname + "@"
		self.clear_command_dst = "/opt/modules/bigdl-master-angelps/executioninfo/timefile*"
		return

	def fetch(self, slaves):
		for slave in slaves:
			scp_command = self.scp_command_pre + slave + self.scp_command_src + " " + self.scp_command_dst + " 2>/dev/null"
			print scp_command
			os.popen(scp_command)
			clear_command = self.clear_command_pre + slave + " rm -rf " + self.clear_command_dst + " 2>/dev/null"
			print clear_command
			os.popen(clear_command)

if __name__ == "__main__":
	theConf = Configuration()
	theFetch = FetchRemoteFiles(theConf.hostname)	
	theFetch.fetch(theConf.slaves)

