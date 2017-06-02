


class HadoopVersion:

	hadoopversion = "2.8.0"
	purpose = "spark"

	absolutepath = "/opt/modules"

	cluster = "Pseudo-distributed"

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

