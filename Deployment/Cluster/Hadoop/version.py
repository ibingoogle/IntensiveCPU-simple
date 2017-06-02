


class HadoopVersion:

	gatherprefix = "sean@sean:"	
	scatterprefix = ""

	hostname = "hadoop0master"
	slaves = ["hadoop1slave1","hadoop1slave2","hadoop1slave3","hadoop1slave4","hadoop1slave5","hadoop1slave6"]
	
	hadoopversion = "2.8.0"
	purpose = "spark"

	absolutepath = "/opt/modules"

	cluster = "Cluster1"

	moduledirname = ""
	hadoopdirname = ""

	modulepath = ""
	hadooppath = ""

	def __init__(self):
		self.set_name_path()
		return

	def set_name_path(self):
		self.moduledirname = "hadoop-" + self.hadoopversion + "-" + self.purpose
		self.hadoopdirname = "hadoop-" + self.hadoopversion

		self.modulepath = self.absolutepath + "/" + self.moduledirname
		self.hadooppath = self.modulepath + "/" + self.hadoopdirname

	def set_scatterprefix(self,theslave):
		self.scatterprefix = self.hostname + "@" + theslave + ":"

