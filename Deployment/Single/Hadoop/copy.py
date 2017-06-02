from version import HadoopVersion
import os
import sys

class CopyConf:

	conf_src_path = ""
	conf_dest_path = ""

	def __init__(self):
		return

	def set_conf_path(self,theVersion):
		self.conf_src_path = theVersion.modulepath + "/ConfigurationFile/" + theVersion.cluster + "/*"
		self.conf_dest_path = theVersion.hadooppath + "/etc/hadoop/"

	def print_conf_path(self):
		print "conf_src_path: ", self.conf_src_path
		print "conf_dest_path: ", self.conf_dest_path

	def copy_conf(self):
		command_copy = "cp " + self.conf_src_path + " " + self.conf_dest_path
		os.popen(command_copy)


def check_args(argv):
	if (len(argv) == 1) and (argv[0] == "conf"):
		return 0
	print_usage()
	sys.exit(2)

def print_usage():
	print "copy.sh - tool for" 
	print "copying configuration to HADOOP_HOME/etc/hadoop"
	print "usage:"
	options="conf"
	print "./copy.sh", options

if __name__ == "__main__":

	check_args(sys.argv[1:])

	theCopyConf = CopyConf()
	theVersion = HadoopVersion()

	theCopyConf.set_conf_path(theVersion)
	
	theCopyConf.copy_conf()
