class Configuration:

	Iter_file = ''
	IterStages_file = ''
	IterStagesNet_file = ''

	hostname = ""
	slaves = []

	def __init__(self):
		self.Size_file = '/opt/modules/bigdl-master-angelps/executioninfo/sizefile.txt'

		self.Iter_file = '/opt/modules/bigdl-master-angelps/executioninfo/timefile.txt'
		self.Iter_Stage_file_pre = '/opt/modules/bigdl-master-angelps/executioninfo/timefile_'
		
		self.Iter_Stage_Net1_file_pre = '/opt/modules/bigdl-master-angelps/executioninfo/timefile_gwcommunication_'
		self.Iter_Stage_Net1_GB_file_pre = '/opt/modules/bigdl-master-angelps/executioninfo/timefile_gwcommunication_gb_'
		self.Iter_Stage_Net1_DC_file_pre = '/opt/modules/bigdl-master-angelps/executioninfo/timefile_gwcommunication_dc_'

		self.Iter_Stage_Net2_file_pre = '/opt/modules/bigdl-master-angelps/executioninfo/timefile_agcommunication_'
		self.Iter_Stage_Net2_Reduce_file_pre = '/opt/modules/bigdl-master-angelps/executioninfo/timefile_agreduce_'
		
		self.Iter_Compute1_file_pre = '/opt/modules/bigdl-master-angelps/executioninfo/timefile_forward_'
		self.Iter_Compute2_file_pre = '/opt/modules/bigdl-master-angelps/executioninfo/timefile_backward_'

		self.Iter_Sparsity1_file_pre = '/opt/modules/bigdl-master-angelps/executioninfo/timefile_sparsity_larger_'
		self.Iter_Sparsity2_file_pre = '/opt/modules/bigdl-master-angelps/executioninfo/timefile_sparsity_between_'

		self.hostname = "hadoop0master"
		#self.slaves = ["hadoop1slave1","hadoop1slave2","hadoop1slave3","hadoop1slave4","hadoop1slave5","hadoop1slave6"]
		#self.slaves = ["hadoop1slave1", "hadoop1slave2", "hadoop1slave3", "hadoop1slave4",  "hadoop1slave5", "hadoop1slave6", "hadoop1slave7", "hadoop1slave8", "hadoop1slave9", "hadoop1slave10", "hadoop1slave11", "hadoop1slave12", "hadoop1slave13", "hadoop1slave14", "hadoop1slave15", "hadoop1slave16", "hadoop1slave17", "hadoop1slave18"]

		# 36 slaves
		self.slaves = ["hadoop1slave1", "hadoop1slave2", "hadoop1slave3", "hadoop1slave4",  "hadoop1slave5", "hadoop1slave6", "hadoop1slave7", "hadoop1slave8", "hadoop1slave9", "hadoop1slave10", "hadoop1slave11", "hadoop1slave12", "hadoop1slave13", "hadoop1slave14", "hadoop1slave15", "hadoop1slave16", "hadoop1slave17", "hadoop1slave18", "hadoop1slave19", "hadoop1slave20", "hadoop1slave21", "hadoop1slave22",  "hadoop1slave23", "hadoop1slave24", "hadoop1slave25", "hadoop1slave26", "hadoop1slave27", "hadoop1slave28", "hadoop1slave29", "hadoop1slave30", "hadoop1slave31", "hadoop1slave32", "hadoop1slave33", "hadoop1slave34", "hadoop1slave35", "hadoop1slave36"]
		return
