from version import HadoopVersion
import os
import sys

class ClusterCopyConf:

	conf_gather_src = ""
	conf_gather_dest = ""

	conf_scatter_src = ""
	conf_scatter_dest = ""

	def __init__(self):
		return

	def set_conf_gather(self,theVersion):
		self.conf_gather_src = theVersion.gatherprefix + theVersion.modulepath + "/ConfigurationFile/" + theVersion.cluster + "/*"
		self.conf_gather_dest = theVersion.hadooppath + "/etc/hadoop/"

	def set_conf_scatter(self,theVersion):
		self.conf_scatter_src = theVersion.hadooppath + "/etc/hadoop/*"
		self.conf_scatter_dest = theVersion.scatterprefix + theVersion.hadooppath + "/etc/hadoop/"

	def print_conf(self):
		print "conf_gather_src: ", self.conf_gather_src
		print "conf_gather_dest: ", self.conf_gather_dest
		print "conf_scatter_src: ", self.conf_scatter_src
		print "conf_scatter_dest: ", self.conf_scatter_dest

	def copy_conf(self,theVersion):
		command_copy_gather = "scp " + self.conf_gather_src + " " + self.conf_gather_dest
		os.popen(command_copy_gather)
		for slave in theVersion.slaves:
			theVersion.set_scatterprefix(slave)
			self.set_conf_scatter(theVersion)
			command_copy_scatter = "scp " + self.conf_scatter_src + " " + self.conf_scatter_dest
			os.popen(command_copy_scatter)


def check_args(argv):
	if (len(argv) == 1) and (argv[0] == "conf"):
		return 0
	print_usage()
	sys.exit(2)

def print_usage():
	print "copy.sh - tool for" 
	print "copying configuration to HADOOP_HOME/etc/hadoop in distributed clusters"
	print "usage:"
	options="conf"
	print "./copy.sh", options

if __name__ == "__main__":

	check_args(sys.argv[1:])

	theCopyConf = ClusterCopyConf()
	theVersion = HadoopVersion()

	theCopyConf.set_conf_gather(theVersion)
	
	theCopyConf.copy_conf(theVersion)
