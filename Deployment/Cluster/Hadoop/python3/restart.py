from version import HadoopVersion
from stop import ClusterStop
from start import ClusterStart
from copy import ClusterCopyAll
import os
import sys
import re

class ClusterRestart:

	def __init__(self):
		self.theStart = ClusterStart()
		self.theStop = ClusterStop()
		self.theCopyAll = ClusterCopyAll()
		return

	def set_shells(self,theVersion):
		self.theCopyAll.set_conf_gather(theVersion)
		self.theCopyAll.set_pkg_gather(theVersion)
		self.theStart.set_shells(theVersion)
		self.theStop.set_shells(theVersion)

	def copy(self,copyresult,theVersion):
		if copyresult == "conf":
			self.theCopyAll.copy_conf(theVersion)
		if copyresult == "all":
			self.theCopyAll.copy_pkg(theVersion)
			self.theCopyAll.copy_conf(theVersion)

	def restart_hdfs(self,copyresult,theVersion):
		self.theStop.stop_hdfs()
		self.copy(copyresult,theVersion)
		self.theStart.start_hdfs()

	def restart_all(self,copyresult,theVersion):
		self.theStop.stop_all()
		self.copy(copyresult,theVersion)
		self.theStart.start_all()

	def restart_yarn(self,copyresult,theVersion):
		self.theStop.stop_yarn()
		self.copy(copyresult,theVersion)
		self.theStart.start_yarn()

def check_args(argv):
	result = []
	if len(argv) > 0 and re.search(r'^(all)$|^(hdfs)$|^(yarn)$', argv[0]) != None:
		result.append(argv[0])
		if len(argv) == 1:
			return result
		if len(argv) == 2 and argv[1] == "conf":
			result.append(argv[1])
			return result
		if len(argv) == 2 and argv[1] == "all":
			result.append(argv[1])
			return result
	print_usage()
	sys.exit(2)

def print_usage():
	print ("restart.sh - tool for")
	print ("restart start/stop commands HADOOP_HOME/sbin")
	print ("usage:")
	options="all/hdfs/yarn [conf/all]"
	print ("./restart.sh", options)

if __name__ == "__main__":

	result = check_args(sys.argv[1:])

	theVersion = HadoopVersion()
	theRestart = ClusterRestart()

	theRestart.set_shells(theVersion)

	copyresult = "none"
	if len(result) == 2:
		copyresult = result[1]

	if result[0] == "all":
		theRestart.restart_all(copyresult,theVersion)
	elif result[0] == "hdfs":
		theRestart.restart_hdfs(copyresult,theVersion)
	elif result[0] == "yarn":
		theRestart.restart_yarn(copyresult,theVersion)
