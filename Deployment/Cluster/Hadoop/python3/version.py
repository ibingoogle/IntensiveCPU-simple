


class HadoopVersion:

	gatherprefix = "sean@sean:"	
	scatterprefix = ""

	hostname = "hadoop0master"
	slaves = ["hadoop2slave1","hadoop2slave2","hadoop2slave3","hadoop2slave4","hadoop2slave5","hadoop2slave6"]
	
	hadoopversion = "2.7.2"
	purpose = "modified"
	suffix = "tar.gz"

	absolutepath = "/opt/modules"

	cluster = "Cluster2"

	moduledirname = ""
	hadoopdirname = ""
	hadooppkgname = ""

	modulepath = ""
	hadooppath = ""
	hadooppkgpath = ""

	def __init__(self):
		self.set_name_path()
		return

	def set_name_path(self):
		self.moduledirname = "hadoop-" + self.hadoopversion + "-" + self.purpose
		self.hadoopdirname = "hadoop-" + self.hadoopversion
		self.hadooppkgname = self.hadoopdirname + "." + self.suffix

		self.modulepath = self.absolutepath + "/" + self.moduledirname
		self.hadooppath = self.modulepath + "/" + self.hadoopdirname
		self.hadooppkgpath = self.modulepath + "/" + self.suffix

	def set_scatterprefix(self,theslave):
		self.scatterprefix = self.hostname + "@" + theslave + ":"

