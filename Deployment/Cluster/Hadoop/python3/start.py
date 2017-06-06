from version import HadoopVersion
import os
import sys


class ClusterStart:

	shell_starthdfs = ""
	shell_startyarn = ""
	shell_starthist = ""

	def __init__(self):
		return

	def set_shells(self,theVersion):
		self.shell_starthdfs = theVersion.hadooppath + "/sbin/start-dfs.sh"
		self.shell_startyarn = theVersion.hadooppath + "/sbin/start-yarn.sh"
		self.shell_starthist = theVersion.hadooppath + "/sbin/mr-jobhistory-daemon.sh start historyserver"

	def start_hdfs(self):
		os.system(self.shell_starthdfs)

	def start_yarn(self):
		os.system(self.shell_startyarn)
		os.system(self.shell_starthist)

	def start_all(self):
		os.system(self.shell_starthdfs)
		os.system(self.shell_startyarn)
		os.system(self.shell_starthist)

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
	print ("start.sh - tool for")
	print ("run start commands HADOOP_HOME/sbin")
	print ("usage:")
	options="all/hdfs/yarn"
	print ("./start.sh", options)

if __name__ == "__main__":

	result = check_args(sys.argv[1:])

	theVersion = HadoopVersion()
	theStart = ClusterStart()

	theStart.set_shells(theVersion)

	if result == 0:
		theStart.start_all()
	elif result == 1:
		theStart.start_hdfs()
	elif result == 2:
		theStart.start_yarn()
