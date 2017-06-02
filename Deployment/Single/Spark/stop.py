from version import SparkVersion
import os
import sys


class Stop:

	shell_stopmaster = ""
	shell_stopslaves = ""
	shell_stophist = ""

	def __init__(self):
		return

	def set_shells(self,theVersion):
		self.shell_stopmaster = theVersion.sparkpath + "/sbin/stop-master.sh"
		self.shell_stopslaves = theVersion.sparkpath + "/sbin/stop-slaves.sh"
		self.shell_stophist = theVersion.sparkpath + "/sbin/stop-history-server.sh"

	def stop_all(self):
		os.system(self.shell_stophist)
		os.system(self.shell_stopslaves)
		os.system(self.shell_stopmaster)

	def stop_standalone(self):
		os.system(self.shell_stopslaves)
		os.system(self.shell_stopmaster)

	def stop_hist(self):
		os.system(self.shell_stophist)

def check_args(argv):
	if len(argv) == 1:
		if argv[0] == "all":
			return 0
		if argv[0] == "standalone":
			return 1
		if argv[0] == "history":
			return 2
	print_usage()
	sys.exit(2)

def print_usage():
	print "stop.sh - tool for" 
	print "run stop commands SPARK_HOME/sbin"
	print "usage:"
	options="all/standalone/history"
	print "./stop.sh", options

if __name__ == "__main__":

	result = check_args(sys.argv[1:])

	theVersion = SparkVersion()
	theStop = Stop()

	theStop.set_shells(theVersion)

	if result == 0:
		theStop.stop_all()
	elif result == 1:
		theStop.stop_standalone()
	elif result == 2:
		theStop.stop_hist()
