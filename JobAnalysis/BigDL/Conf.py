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

		self.hostname = "hadoop0master"
		self.slaves = ["hadoop1slave1","hadoop1slave2","hadoop1slave3","hadoop1slave4","hadoop1slave5","hadoop1slave6"]
		return
