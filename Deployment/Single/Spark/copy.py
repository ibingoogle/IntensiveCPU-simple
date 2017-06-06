from version import SparkVersion
import os
import sys

class CopyConf:

	conf_src_path = ""
	conf_dest_path = ""

	def __init__(self):
		return

	def set_conf_path(self,theVersion):
		self.conf_src_path = theVersion.modulepath + "/ConfigurationFile/" + theVersion.cluster + "/conf/*"
		self.conf_dest_path = theVersion.sparkpath + "/conf/"

	def print_conf_path(self):
		print "conf_src_path: ", self.conf_src_path
		print "conf_dest_path: ", self.conf_dest_path

	def copy_conf(self):
		command_copy = "cp " + self.conf_src_path + " " + self.conf_dest_path
		os.popen(command_copy)

class CopyAll(CopyConf):

	pkg_src_path = ""
	pkg_dest_path = ""
	sparkpath = ""
	sparkpkgname = ""

	def __init__(self):
		return

	def set_pkg_path(self,theVersion):
		self.pkg_src_path = theVersion.sparkpkgpath + "/*." + theVersion.suffix
		self.pkg_dest_path = theVersion.modulepath
		self.sparkpath = theVersion.sparkpath
		self.sparkpkgname = theVersion.sparkpkgname

	def print_pkg_path(self):
		print "pkg_src_path: ", self.pkg_src_path
		print "pkg_dest_path: ", self.pkg_dest_path

	def copy_pkg(self):
		command_copy = "cp " + self.pkg_src_path + " " + self.pkg_dest_path
		os.popen(command_copy)
		self.rm_extract()

	def rm_extract(self):
		command_rm = "rm -rf " + self.sparkpath + " 2>/dev/null"
		os.popen(command_rm)
		command_extract = "tar zxf " + self.pkg_dest_path + "/" + self.sparkpkgname
		os.popen(command_extract)

def check_args(argv):
	if (len(argv) == 1) and (argv[0] == "conf"):
		return 0
	elif (len(argv) == 2) and (argv[0] == "all"):
		if argv[1] == "SBT":
			return "SBT"
		elif argv[1] == "MVN":
			return "MVN"
	print_usage()
	sys.exit(2)

def print_usage():
	print "copy.sh - tool for" 
	print "(1)copying configuration to SPARK_HOME/conf"
	print "(2)copying and extracting packaged .tgz to SPARK_HOME"
	print "usage:"
	options="conf/(all MVN/SBT)"
	print "./copy.sh", options

if __name__ == "__main__":

	result = check_args(sys.argv[1:])

	theCopyAll = CopyAll()
	theVersion = SparkVersion()

	theCopyAll.set_conf_path(theVersion)

	if result == 0:
		theCopyAll.copy_conf()
	else:
		theVersion.set_buildversion(result)
		theCopyAll.set_pkg_path(theVersion)
		theCopyAll.copy_pkg()
		theCopyAll.copy_conf()
