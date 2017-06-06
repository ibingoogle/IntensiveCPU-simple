


class HadoopVersion:

	hadoopversion = "2.7.2"
	purpose = "modified"

	absolutepath = "/opt/modules"

	cluster = "Pseudo-distributed"
	suffix = "tar.gz"

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

