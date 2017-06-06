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
		print command_copy
		os.popen(command_copy)


class CopyAll(CopyConf):

	pkg_src_path = ""
	pkg_dest_path = ""
	hadooppath = ""
	hadooppkgname = ""

	def __init__(self):
		return

	def set_pkg_path(self,theVersion):
		self.pkg_src_path = theVersion.hadooppkgpath + "/*." + theVersion.suffix
		self.pkg_dest_path = theVersion.modulepath
		self.hadooppath = theVersion.hadooppath
		self.hadooppkgname = theVersion.hadooppkgname

	def print_pkg_path(self):
		print "pkg_src_path: ", self.pkg_src_path
		print "pkg_dest_path: ", self.pkg_dest_path

	def copy_pkg(self):
		command_copy = "cp " + self.pkg_src_path + " " + self.pkg_dest_path
		print command_copy
		os.popen(command_copy)
		self.rm_extract()

	def rm_extract(self):
		command_rm = "rm -rf " + self.hadooppath + " 2>/dev/null"
		print command_rm
		os.popen(command_rm)
		command_extract = "tar zxf " + self.pkg_dest_path + "/" + self.hadooppkgname
		print command_extract
		os.popen(command_extract)

def check_args(argv):
	if len(argv) == 1:
		if argv[0] == "conf":
			return 0
		elif argv[0] == "all":
			return 1
	print_usage()
	sys.exit(2)

def print_usage():
	print "copy.sh - tool for" 
	print "(1)copying configuration to HADOOP_HOME/conf"
	print "(2)copying and extracting packaged .tgz to HADOOP_HOME"
	print "usage:"
	options="conf/all"
	print "./copy.sh", options

if __name__ == "__main__":

	result = check_args(sys.argv[1:])

	theCopyAll = CopyAll()
	theVersion = HadoopVersion()

	theCopyAll.set_conf_path(theVersion)
	theCopyAll.set_pkg_path(theVersion)

	if result == 0:
		theCopyAll.copy_conf()
	else:
		theCopyAll.copy_pkg()
		theCopyAll.copy_conf()
