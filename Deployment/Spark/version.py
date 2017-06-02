


class SparkVersion:

	gatherprefix = "sean@sean:"	
	scatterprefix = ""

	hostname = "hadoop0master"
	slaves = ["hadoop1slave1","hadoop1slave2","hadoop1slave3","hadoop1slave4","hadoop1slave5","hadoop1slave6"]

	sparkversion = "2.1.1"
	hadoopversion = "2.8.0"
	purpose = "modified"

	buildversion = "SBT"
	suffix = "tgz"
	absolutepath = "/opt/modules"

	cluster = "Cluster1"

	moduledirname = ""
	sparkdirname = ""
	sparkpkgname = ""

	modulepath = ""
	sparkpath = ""
	sparkpkgpath = ""

	def __init__(self):
		self.set_name_path()
		return

	def set_name_path(self):
		self.moduledirname = "spark-" + self.sparkversion + "-" + self.purpose
		self.sparkdirname = "spark-" + self.sparkversion + "-bin-" + self.hadoopversion
		self.sparkpkgname = self.sparkdirname + "." + self.suffix

		self.modulepath = self.absolutepath + "/" + self.moduledirname
		self.sparkpath = self.modulepath + "/" + self.sparkdirname
		self.sparkpkgpath = self.modulepath + "/" + self.suffix + "/" + self.buildversion

	def set_buildversion(self,newbuild):
		self.buildversion = newbuild
		self.set_name_path()

	def set_scatterprefix(self,theslave):
		self.scatterprefix = self.hostname + "@" + theslave + ":"
