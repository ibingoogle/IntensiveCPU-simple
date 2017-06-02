from version import SparkVersion
import os
import sys


class Start:

	shell_startmaster = ""
	shell_startslaves = ""
	shell_starthist = ""

	def __init__(self):
		return

	def set_shells(self,theVersion):
		self.shell_startmaster = theVersion.sparkpath + "/sbin/start-master.sh"
		self.shell_startslaves = theVersion.sparkpath + "/sbin/start-slaves.sh"
		self.shell_starthist = theVersion.sparkpath + "/sbin/start-history-server.sh"

	def start_all(self):
		os.system(self.shell_startmaster)
		os.system(self.shell_startslaves)
		os.system(self.shell_starthist)

	def start_standalone(self):
		os.system(self.shell_startmaster)
		os.system(self.shell_startslaves)

	def start_hist(self):
		os.system(self.shell_starthist)


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
	print "start.sh - tool for" 
	print "run start commands SPARK_HOME/sbin"
	print "usage:"
	options="all/standalone/history"
	print "./start.sh", options

if __name__ == "__main__":

	result = check_args(sys.argv[1:])

	theVersion = SparkVersion()
	theStart = Start()

	theStart.set_shells(theVersion)

	if result == 0:
		theStart.start_all()
	elif result == 1:
		theStart.start_standalone()
	elif result == 2:
		theStart.start_hist()
