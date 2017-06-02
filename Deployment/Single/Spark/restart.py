from version import SparkVersion
from copy import CopyAll
from start import Start
from stop import Stop
import os
import sys
import re


class Restart:

	def __init__(self):
		self.theCopyAll = CopyAll()
		self.theStart = Start()
		self.theStop = Stop()
		return

	def set_shells(self,theVersion):
		self.theCopyAll.set_conf_path(theVersion)
		self.theCopyAll.set_pkg_path(theVersion)
		self.theStart.set_shells(theVersion)
		self.theStop.set_shells(theVersion)

	def copy(self,copyresult):
		if copyresult == "conf":
			self.theCopyAll.copy_conf()
		elif copyresult == "all":
			self.theCopyAll.copy_pkg()
			self.theCopyAll.copy_conf()

	def restart_all(self,copyresult):
		self.theStop.stop_all()
		self.copy(copyresult)
		self.theStart.start_all()

	def restart_standalone(self,copyresult):
		self.theStop.stop_standalone()
		self.copy(copyresult)
		self.theStart.start_standalone()

	def restart_hist(self,copyresult):
		self.theStop.stop_hist()
		self.copy(copyresult)
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
	theRestart = Restart()

	if len(result) == 3:
		theVersion.set_buildversion(result[2])
	theRestart.set_shells(theVersion)

	copyresult = "none"
	if len(result) > 1:
		copyresult = result[1]

	if result[0] == "all":
		theRestart.restart_all(copyresult)
	elif result[0] == "standalone":
		theRestart.restart_standalone(copyresult)
	elif result[0] == "history":
		theRestart.restart_hist(copyresult)
