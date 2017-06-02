from version import SparkVersion
from copy import ClusterCopyAll
from start import ClusterStart
from stop import ClusterStop
import os
import sys
import re


class ClusterRestart:

	def __init__(self):
		self.theCopyAll = ClusterCopyAll()
		self.theStart = ClusterStart()
		self.theStop = ClusterStop()
		return

	def set_shells(self,theVersion):
		self.theCopyAll.set_conf_gather(theVersion)
		self.theCopyAll.set_pkg_gather(theVersion)
		self.theStart.set_shells(theVersion)
		self.theStop.set_shells(theVersion)

	def copy(self,copyresult,theVersion):
		if copyresult == "conf":
			self.theCopyAll.copy_conf(theVersion)
		elif copyresult == "all":
			self.theCopyAll.copy_pkg(theVersion)
			self.theCopyAll.copy_conf(theVersion)

	def restart_all(self,copyresult,theVersion):
		self.theStop.stop_all()
		self.copy(copyresult,theVersion)
		self.theStart.start_all()

	def restart_standalone(self,copyresult,theVersion):
		self.theStop.stop_standalone()
		self.copy(copyresult,theVersion)
		self.theStart.start_standalone()

	def restart_hist(self,copyresult,theVersion):
		self.theStop.stop_hist()
		self.copy(copyresult,theVersion)
		self.theStart.start_hist()

def check_args(argv):
	result = []
	if len(argv) > 0 and re.search(r'^(all)$|^(standalone)$|^(history)$', argv[0]) != None:
		result.append(argv[0])
		if len(argv) == 1:
			return result
		if (len(argv) == 2) and (argv[1] == "conf"):
			result.append(argv[1])
			return result
		if (len(argv) == 3) and (argv[1] == "all"):
			result.append(argv[1])
			if argv[2] == "SBT":
				result.append(argv[2])
				return result
			elif argv[2] == "MVN":
				result.append(argv[2])
				return result
	print_usage()
	sys.exit(2)

def print_usage():
	print "restart.sh - tool for" 
	print "restart stop/start commands HADOOP_HOME/sbin"
	print "usage:"
	options="all/standalone/history [conf/(all MVN/SBT)]"
	print "./restart.sh", options

if __name__ == "__main__":

	result = check_args(sys.argv[1:])

	theVersion = SparkVersion()
	theRestart = ClusterRestart()

	if len(result) == 3:
		theVersion.set_buildversion(result[2])
	theRestart.set_shells(theVersion)

	copyresult = "none"
	if len(result) > 1:
		copyresult = result[1]

	if result[0] == "all":
		theRestart.restart_all(copyresult,theVersion)
	elif result[0] == "standalone":
		theRestart.restart_standalone(copyresult,theVersion)
	elif result[0] == "history":
		theRestart.restart_hist(copyresult,theVersion)
