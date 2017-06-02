from version import HadoopVersion
import os
import sys


class Stop:

	shell_stophdfs = ""
	shell_stopyarn = ""
	shell_stophist = ""

	def __init__(self):
		return

	def set_shells(self,theVersion):
		self.shell_stophdfs = theVersion.hadooppath + "/sbin/stop-dfs.sh"
		self.shell_stopyarn = theVersion.hadooppath + "/sbin/stop-yarn.sh"
		self.shell_stophist = theVersion.hadooppath + "/sbin/mr-jobhistory-daemon.sh stop historyserver"

	def stop_hdfs(self):
		os.system(self.shell_stophdfs)

	def stop_yarn(self):
		os.system(self.shell_stophist)
		os.system(self.shell_stopyarn)

	def stop_all(self):
		os.system(self.shell_stophist)
		os.system(self.shell_stopyarn)
		os.system(self.shell_stophdfs)

def check_args(argv):
	if len(argv) == 1:
		if argv[0] == "all":
			return 0
		if argv[0] == "hdfs":
			return 1
		if argv[0] == "yarn":
			return 2
	print_usage()
	sys.exit(2)

def print_usage():
	print "stop.sh - tool for" 
	print "run stop commands HADOOP_HOME/sbin"
	print "usage:"
	options="all/hdfs/yarn"
	print "./stop.sh", options

if __name__ == "__main__":

	result = check_args(sys.argv[1:])

	theVersion = HadoopVersion()
	theStop = Stop()

	theStop.set_shells(theVersion)

	if result == 0:
		theStop.stop_all()
	elif result == 1:
		theStop.stop_hdfs()
	elif result == 2:
		theStop.stop_yarn()
