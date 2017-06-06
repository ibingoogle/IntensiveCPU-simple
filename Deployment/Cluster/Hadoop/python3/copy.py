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
		print ("conf_gather_src: ", self.conf_gather_src)
		print ("conf_gather_dest: ", self.conf_gather_dest)
		print ("conf_scatter_src: ", self.conf_scatter_src)
		print ("conf_scatter_dest: ", self.conf_scatter_dest)

	def copy_conf(self,theVersion):
		command_copy_gather = "scp " + self.conf_gather_src + " " + self.conf_gather_dest
		os.popen(command_copy_gather)
		print (command_copy_gather)
		for slave in theVersion.slaves:
			theVersion.set_scatterprefix(slave)
			self.set_conf_scatter(theVersion)
			command_copy_scatter = "scp " + self.conf_scatter_src + " " + self.conf_scatter_dest
			print (command_copy_scatter)
			os.popen(command_copy_scatter)


class ClusterCopyAll(ClusterCopyConf):

	pkg_gather_src = ""
	pkg_gather_dest = ""

	pkg_scatter_src = ""
	pkg_scatter_dest = ""

	hadooppath = ""
	hadooppkgname = ""

	def __init__(self):
		return

	def set_pkg_gather(self,theVersion):
		self.pkg_gather_src = theVersion.gatherprefix + theVersion.hadooppkgpath + "/*." + theVersion.suffix
		self.pkg_gather_dest = theVersion.modulepath
		self.hadooppath = theVersion.hadooppath
		self.hadooppkgname = theVersion.hadooppkgname

	def set_pkg_scatter(self,theVersion):
		self.pkg_scatter_src = theVersion.modulepath + "/*." + theVersion.suffix
		self.pkg_scatter_dest = theVersion.scatterprefix + theVersion.modulepath

	def print_pkg_path(self):
		print ("pkg_gather_src: ", self.pkg_gather_src)
		print ("pkg_gather_dest: ", self.pkg_gather_dest)
		print ("pkg_scatter_src: ", self.pkg_scatter_src)
		print ("pkg_scatter_dest: ", self.pkg_scatter_dest)

	def copy_pkg(self,theVersion):
		command_copy_gather = "scp " + self.pkg_gather_src + " " + self.pkg_gather_dest
		print (command_copy_gather)
		os.popen(command_copy_gather)
		self.gather_rm_extract()
		for slave in theVersion.slaves:
			theVersion.set_scatterprefix(slave)
			self.set_pkg_scatter(theVersion)
			command_copy_scatter = "scp " + self.pkg_scatter_src + " " + self.pkg_scatter_dest
			print (command_copy_scatter)
			os.popen(command_copy_scatter)
			self.scatter_rm_extract(theVersion)


	def gather_rm_extract(self):
		command_rm_gather = "rm -rf " + self.hadooppath + " 2>/dev/null"
		print (command_rm_gather)
		os.popen(command_rm_gather)
		command_extract_gather = "tar zxf " + self.pkg_gather_dest + "/" + self.hadooppkgname
		print (command_extract_gather)
		os.popen(command_extract_gather)

	def scatter_rm_extract(self,theVersion):
		command_rm_scatter = "ssh " + theVersion.scatterprefix[0:len(theVersion.scatterprefix)-1] + " rm -f " + theVersion.hadooppath + " 2>/dev/null"
		print (command_rm_scatter)
		os.popen(command_rm_scatter)
		command_extract_scatter = "ssh " + theVersion.scatterprefix[0:len(theVersion.scatterprefix)-1] + " tar zxf " + theVersion.modulepath + "/" + theVersion.hadooppkgname + " -C " + theVersion.modulepath + "/"
		print (command_extract_scatter)
		os.popen(command_extract_scatter)


def check_args(argv):
	if (len(argv) == 1) and (argv[0] == "conf"):
		return 0
	print_usage()
	sys.exit(2)

def check_args(argv):
	if len(argv) == 1: 
		if argv[0] == "conf":
			return 0
		elif argv[0] == "all":
			return 1
	print_usage()
	sys.exit(2)

def print_usage():
	print ("copy.sh - tool for")
	print ("(1)copying configuration to HADOOP_HOME/etc/hadoop in distributed clusters")
	print ("(2)copying and extracting packaged .tgz to SPARK_HOME in distributed clusters")
	print ("usage:")
	options="conf/all"
	print ("./copy.sh", options)

if __name__ == "__main__":

	result = check_args(sys.argv[1:])

	theCopyAll = ClusterCopyAll()
	theVersion = HadoopVersion()

	theCopyAll.set_conf_gather(theVersion)
	theCopyAll.set_pkg_gather(theVersion)

	if result == 0:
		theCopyAll.copy_conf(theVersion)
	else:
		theCopyAll.copy_pkg(theVersion)
		theCopyAll.copy_conf(theVersion)
