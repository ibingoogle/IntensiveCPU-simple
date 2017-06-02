from version import HadoopVersion
from stop import Stop
from start import Start
from copy import CopyConf
import os
import sys
import re

class Restart:

	def __init__(self):
		self.theStart = Start()
		self.theStop = Stop()
		self.theCopyConf = CopyConf()
		return

	def set_shells(self,theVersion):
		self.theCopyConf.set_conf_path(theVersion)
		self.theStart.set_shells(theVersion)
		self.theStop.set_shells(theVersion)

	def copy(self,copyresult):
		if copyresult == "conf":
			self.theCopyConf.copy_conf()

	def restart_hdfs(self,copyresult):
		self.theStop.stop_hdfs()
		self.copy(copyresult)
		self.theStart.start_hdfs()

	def restart_all(self,copyresult):
		self.theStop.stop_all()
		self.copy(copyresult)
		self.theStart.start_all()

	def restart_yarn(self,copyresult):
		self.theStop.stop_yarn()
		self.copy(copyresult)
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
	print_usage()
	sys.exit(2)

def print_usage():
	print "restart.sh - tool for" 
	print "restart start/stop commands HADOOP_HOME/sbin"
	print "usage:"
	options="all/hdfs/yarn [conf]"
	print "./restart.sh", options

if __name__ == "__main__":

	result = check_args(sys.argv[1:])

	theVersion = HadoopVersion()
	theRestart = Restart()

	theRestart.set_shells(theVersion)

	copyresult = "none"
	if len(result) == 2:
		copyresult = result[1]

	if result[0] == "all":
		theRestart.restart_all(copyresult)
	elif result[0] == "hdfs":
		theRestart.restart_hdfs(copyresult)
	elif result[0] == "yarn":
		theRestart.restart_yarn(copyresult)
