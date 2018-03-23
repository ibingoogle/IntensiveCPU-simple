import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from Iteration import IterTime
from IterationStage import IterStageTime
from IterationStageNet1 import IterStageNet1Time
from IterationStageNet1GB import IterStageNet1GBTime
from IterationStageNet1DC import IterStageNet1DCTime
from IterationStageNet2 import IterStageNet2Time
from IterationStageNet2Reduce import IterStageNet2ReduceTime
from IterationCompute1 import IterCompute1Time
from IterationCompute2 import IterCompute2Time
from Conf import Configuration

class AppTime:

	ParaSize = []
	GradSize = []
	ParaSize_norm = []
	GradSize_norm = []
	
	Iters = []

	ItersStages = []

	ItersStagesNet1 = []
	ItersStagesNet1GB = []
	ItersStagesNet1DC = []

	ItersStagesNet2 = []
	ItersStagesNet2Reduce = []

	ItersCompute1 = []
	ItersCompute2 = []

	executor_label = []

	def __init__(self):
		return

	def load_Size(self, filename):
		f = open(filename)
		line1 = f.readline()
		paraline = line1.split(" = ")[1]
		sp_paraline = paraline.split(" , ")
		for index in range(len(sp_paraline)-1):
			self.ParaSize.append(sp_paraline[index])
		line2 = f.readline()
		gradline = line2.split(" = ")[1]
		sp_gradline = gradline.split(" , ")
		for index in range(len(sp_gradline)-1):
			self.GradSize.append(sp_gradline[index])
		#print self.ParaSize
		#print self.GradSize

	def norm_Size(self):
		max_parasize = float(self.ParaSize[len(self.ParaSize)-1])
		for index in range(len(self.ParaSize)):
			self.ParaSize_norm.append(float(self.ParaSize[index])/max_parasize + 0.1)
		max_gradsize = float(self.GradSize[len(self.GradSize)-1])
		for index in range(len(self.GradSize)):
			self.GradSize_norm.append(float(self.GradSize[index])/max_gradsize + 0.1)
		#print self.ParaSize_norm
		#print self.GradSize_norm

	def load_Iters(self, filename):
		f = open(filename)
		for line in f.readlines():
			sp_line = line.strip("\n").split(" && ")
			if len(sp_line) == 2:
				theIterTime = IterTime()
				theIterTime.set_times(sp_line[1])
				self.Iters.append(theIterTime)

	def plot_Iter(self, num):
		theIterTime = self.Iters[num-1]
		plt.bar(range(len(theIterTime.list_time)), theIterTime.list_time, color='brbrb')
		plt.show()
		return

	def load_executor_label(self, executor_file_pre, slaves):
		for slave in slaves:
			filename = executor_file_pre + slave + '.txt'
			if os.path.isfile(filename):
				self.executor_label.append(slave)
				#print filename

	def load_ItersStages(self, Iter_Stage_file_pre):
		for executor in self.executor_label:
			filename = Iter_Stage_file_pre + executor + '.txt'
			f = open(filename)
			i = 0
			for line in f.readlines():
				if len(self.ItersStages) <= i:
					theIterStageTime = IterStageTime()
					theIterStageTime.add_times(executor, line)
					self.ItersStages.append(theIterStageTime)
				else:
					theIterStageTime = self.ItersStages[i]
					theIterStageTime.add_times(executor, line)
				i = i + 1

	def print_ItersStages_all(self):
		for theIterStageTime in self.ItersStages:
			theIterStageTime.print_times()

	def print_ItersStages(self, num):
		self.ItersStages[num-1].print_times()

	def plot_ItersStages_stage1(self, num):
		theIterStageTime = self.ItersStages[num-1]
		list_time_1 = []
		list_time_2 = []
		list_time_3 = []
		for executor in theIterStageTime.executor_label:
			list_time_1.append(theIterStageTime.dict_time_stage1[executor][0])
			list_time_2.append(theIterStageTime.dict_time_stage1[executor][1])
			list_time_3.append(theIterStageTime.dict_time_stage1[executor][2])
		l1 = np.array(list_time_1)
		l2 = np.array(list_time_2)
		l3 = np.array(list_time_3)
		plt.bar(range(len(list_time_1)), l1, label='getweights', color = 'b')
		plt.bar(range(len(list_time_1)), l2, bottom = l1, label='computing', color = 'r')
		plt.bar(range(len(list_time_1)), l3, bottom = l1+l2, label='localaggput', color = 'y')
		plt.show()

	def plot_ItersStages_stage2(self, num):
		theIterStageTime = self.ItersStages[num-1]
		list_time_1 = []
		list_time_2 = []
		list_time_3 = []
		list_time_4 = []
		for executor in theIterStageTime.executor_label:
			list_time_1.append(theIterStageTime.dict_time_stage2[executor][0])
			list_time_2.append(theIterStageTime.dict_time_stage2[executor][1])
			list_time_3.append(theIterStageTime.dict_time_stage2[executor][2])
			list_time_4.append(theIterStageTime.dict_time_stage2[executor][3])
		l1 = np.array(list_time_1)
		l2 = np.array(list_time_2)
		l3 = np.array(list_time_3)
		l4 = np.array(list_time_4)
		plt.bar(range(len(list_time_1)), l1, label='remoteagg', color = 'b')
		plt.bar(range(len(list_time_1)), l2, bottom = l1, label='reduceagg', color = 'g')
		plt.bar(range(len(list_time_1)), l3, bottom = l1+l2, label='synchronization', color = 'r')
		plt.bar(range(len(list_time_1)), l4, bottom = l1+l2+l3, label='sendweights', color = 'y')
		plt.show()


	def load_ItersStagesNet1(self, Iter_Stage_Net1_file_pre):
		for executor in self.executor_label:
			filename = Iter_Stage_Net1_file_pre + executor + '.txt'
			f = open(filename)
			i = 0
			for line in f.readlines():
				if len(self.ItersStagesNet1) <= i:
					theIterStageNet1Time = IterStageNet1Time()
					theIterStageNet1Time.add_times(executor, line)
					theIterStageNet1Time.norm_times(executor)
					self.ItersStagesNet1.append(theIterStageNet1Time)
				else:
					theIterStageNet1Time = self.ItersStagesNet1[i]
					theIterStageNet1Time.add_times(executor, line)
					theIterStageNet1Time.norm_times(executor)
				i = i + 1
		
	def print_ItersStagesNet1_all(self):
		for theIterStageNet1Time in self.ItersStagesNet1:
			theIterStageNet1Time.print_times()

	def print_ItersStagesNet1(self, num):
		self.ItersStagesNet1[num-1].print_times()

	def plot_ItersStagesNet1(self, num):
		theIterStageNet1Time = self.ItersStagesNet1[num-1]
		for executor in self.executor_label:
			list_time_1 = []
			list_time_2 = []
			block_label = theIterStageNet1Time.dict_block_label[executor]
			time = theIterStageNet1Time.dict_time[executor]
			for blockId in block_label:
				time_start_end = time[blockId]
				list_time_1.append(time_start_end[0])
				list_time_2.append(time_start_end[1] - time_start_end[0])
			plt.bar(range(len(list_time_1)), list_time_2, bottom = list_time_1, label='getblock', color = 'g')
			plt.show()


	def load_ItersStagesNet1GB(self, Iter_Stage_Net1_GB_file_pre):
		for executor in self.executor_label:
			filename = Iter_Stage_Net1_GB_file_pre + executor + '.txt'
			f = open(filename)
			i = 0
			for line in f.readlines():
				if len(self.ItersStagesNet1GB) <= i:
					theIterStageNet1GBTime = IterStageNet1GBTime()
					theIterStageNet1GBTime.add_times(executor, line)
					theIterStageNet1GBTime.norm_times(executor)
					self.ItersStagesNet1GB.append(theIterStageNet1GBTime)
				else:
					theIterStageNet1GBTime = self.ItersStagesNet1GB[i]
					theIterStageNet1GBTime.add_times(executor, line)
					theIterStageNet1GBTime.norm_times(executor)
				i = i + 1
		
	def print_ItersStagesNet1GB_all(self):
		for theIterStageNet1GBTime in self.ItersStagesNet1GB:
			theIterStageNet1GBTime.print_times()

	def print_ItersStagesNet1GB(self, num):
		self.ItersStagesNet1GB[num-1].print_times()

	def plot_ItersStagesNet1GB(self, num):
		theIterStageNet1GBTime = self.ItersStagesNet1GB[num-1]
		for executor in self.executor_label:
			list_time_1 = []
			list_time_2 = []
			block_label = theIterStageNet1GBTime.dict_block_label[executor]
			time = theIterStageNet1GBTime.dict_time[executor]
			for blockId in block_label:
				time_start_end = time[blockId]
				list_time_1.append(time_start_end[0])
				list_time_2.append(time_start_end[1] - time_start_end[0])
			plt.bar(range(len(list_time_1)), list_time_2, bottom = list_time_1, label='getblock', color = 'r')
			plt.show()

	def load_ItersStagesNet1DC(self, Iter_Stage_Net1_DC_file_pre):
		for executor in self.executor_label:
			filename = Iter_Stage_Net1_DC_file_pre + executor + '.txt'
			f = open(filename)
			i = 0
			for line in f.readlines():
				if len(self.ItersStagesNet1DC) <= i:
					theIterStageNet1DCTime = IterStageNet1DCTime()
					theIterStageNet1DCTime.add_times(executor, line)
					theIterStageNet1DCTime.norm_times(executor)
					self.ItersStagesNet1DC.append(theIterStageNet1DCTime)
				else:
					theIterStageNet1DCTime = self.ItersStagesNet1DC[i]
					theIterStageNet1DCTime.add_times(executor, line)
					theIterStageNet1DCTime.norm_times(executor)
				i = i + 1
		
	def print_ItersStagesNet1DC_all(self):
		for theIterStageNet1DCTime in self.ItersStagesNet1DC:
			theIterStageNet1DCTime.print_times()

	def print_ItersStagesNet1DC(self, num):
		self.ItersStagesNet1DC[num-1].print_times()

	def plot_ItersStagesNet1DC(self, num):
		theIterStageNet1DCTime = self.ItersStagesNet1DC[num-1]
		for executor in self.executor_label:
			list_time_1 = []
			list_time_2 = []
			block_label = theIterStageNet1DCTime.dict_block_label[executor]
			time = theIterStageNet1DCTime.dict_time[executor]
			for blockId in block_label:
				time_start_end = time[blockId]
				list_time_1.append(time_start_end[0])
				list_time_2.append(time_start_end[1] - time_start_end[0])
			plt.bar(range(len(list_time_1)), list_time_2, bottom = list_time_1, label='getblock', color = 'y')
			plt.show()

	def load_ItersStagesNet2(self, Iter_Stage_Net2_file_pre):
		for executor in self.executor_label:
			filename = Iter_Stage_Net2_file_pre + executor + '.txt'
			f = open(filename)
			i = 0
			for line in f.readlines():
				if len(self.ItersStagesNet2) <= i:
					theIterStageNet2Time = IterStageNet2Time()
					theIterStageNet2Time.add_times(executor, line)
					theIterStageNet2Time.norm_times(executor)
					self.ItersStagesNet2.append(theIterStageNet2Time)
				else:
					theIterStageNet2Time = self.ItersStagesNet2[i]
					theIterStageNet2Time.add_times(executor, line)
					theIterStageNet2Time.norm_times(executor)
				i = i + 1
		
	def print_ItersStagesNet2_all(self):
		for theIterStageNet2Time in self.ItersStagesNet2:
			theIterStageNet2Time.print_times()

	def print_ItersStagesNet2(self, num):
		self.ItersStagesNet2[num-1].print_times()


	def plot_ItersStagesNet2(self, num):
		theIterStageNet2Time = self.ItersStagesNet2[num-1]
		for executor in self.executor_label:
			list_time_1 = []
			list_time_2 = []
			block_label = theIterStageNet2Time.dict_block_label[executor]
			time = theIterStageNet2Time.dict_time[executor]
			for blockId in block_label:
				time_start_end = time[blockId]
				list_time_1.append(time_start_end[0])
				list_time_2.append(time_start_end[1] - time_start_end[0])
			plt.bar(range(len(list_time_1)), list_time_2, bottom = list_time_1, label='getblock', color = 'b')
			plt.show()


	def load_ItersStagesNet2Reduce(self, Iter_Stage_Net2_Reduce_file_pre):
		for executor in self.executor_label:
			filename = Iter_Stage_Net2_Reduce_file_pre + executor + '.txt'
			f = open(filename)
			i = 0
			for line in f.readlines():
				if len(self.ItersStagesNet2Reduce) <= i:
					theIterStageNet2ReduceTime = IterStageNet2ReduceTime()
					theIterStageNet2ReduceTime.add_times(executor, line)
					self.ItersStagesNet2Reduce.append(theIterStageNet2ReduceTime)
				else:
					theIterStageNet2ReduceTime = self.ItersStagesNet2Reduce[i]
					theIterStageNet2ReduceTime.add_times(executor, line)
				i = i + 1
		
	def print_ItersStagesNet2Reduce_all(self):
		for theIterStageNet2Time in self.ItersStagesNet2:
			theIterStageNet2Time.print_times()

	def print_ItersStagesNet2Reduce(self, num):
		self.ItersStagesNet2[num-1].print_times()


	def load_ItersCompute1(self, Iter_Compute1_file_pre):
		for executor in self.executor_label:
			filename = Iter_Compute1_file_pre + executor + '.txt'
			f = open(filename)
			i = 0
			for line in f.readlines():
				if len(self.ItersCompute1) <= i:
					theIterCompute1Time = IterCompute1Time()
					theIterCompute1Time.add_times(executor, line)
					theIterCompute1Time.norm_times(executor)
					self.ItersCompute1.append(theIterCompute1Time)
				else:
					theIterCompute1Time = self.ItersCompute1[i]
					theIterCompute1Time.add_times(executor, line)
					theIterCompute1Time.norm_times(executor)
				i = i + 1

	def print_ItersCompute1(self, num):
		self.ItersCompute1[num-1].print_times()

	def load_ItersCompute2(self, Iter_Compute2_file_pre):
		for executor in self.executor_label:
			filename = Iter_Compute2_file_pre + executor + '.txt'
			f = open(filename)
			i = 0
			for line in f.readlines():
				if len(self.ItersCompute2) <= i:
					theIterCompute2Time = IterCompute2Time()
					theIterCompute2Time.add_times(executor, line)
					theIterCompute2Time.norm_times(executor)
					self.ItersCompute2.append(theIterCompute2Time)
				else:
					theIterCompute2Time = self.ItersCompute2[i]
					theIterCompute2Time.add_times(executor, line)
					theIterCompute2Time.norm_times(executor)
				i = i + 1

	def print_ItersCompute2(self, num):
		self.ItersCompute2[num-1].print_times()

	def plot_ItersCompute12_norm(self, num):
		theIterCompute1time = self.ItersCompute1[num-1]
		theIterCompute2time = self.ItersCompute2[num-1]
		for executor in self.executor_label:
			time_forward_norm = theIterCompute1time.dict_time_forward_norm[executor]
			time_backward_norm = theIterCompute2time.dict_time_backward_norm[executor]
			size = len(time_forward_norm)
			x = np.arange(size)
			total_width, n = 0.6, 3
			width = total_width / n
			x = x - (total_width - width) / 2
			plt.bar(x, time_forward_norm, width = width, label='forward', color = 'r')
			plt.bar(x + width, time_backward_norm, width = width, label='backward', color = 'b')
			plt.bar(x + 2*width, self.ParaSize_norm, width = width, label='parasize', color = 'g')
			plt.xlim((-1, 17))
			plt.ylim((0.1, 1.5))
			plt.show()


if __name__ == "__main__":

	theAppTime = AppTime()
	theConf = Configuration()

	theAppTime.load_Size(theConf.Size_file)
	theAppTime.norm_Size()

	theAppTime.load_Iters(theConf.Iter_file)
	#theAppTime.plot_Iter(1)

	theAppTime.load_executor_label(theConf.Iter_Stage_file_pre, theConf.slaves)

	theAppTime.load_ItersStages(theConf.Iter_Stage_file_pre)
	#theAppTime.print_ItersStages(1)
	theAppTime.plot_ItersStages_stage1(1)
	theAppTime.plot_ItersStages_stage2(1)

	theAppTime.load_ItersStagesNet1(theConf.Iter_Stage_Net1_file_pre)
	#theAppTime.print_ItersStagesNet1(1)
	#theAppTime.plot_ItersStagesNet1(1)

	theAppTime.load_ItersStagesNet1GB(theConf.Iter_Stage_Net1_GB_file_pre)
	#theAppTime.print_ItersStagesNet1GB(1)
	#theAppTime.plot_ItersStagesNet1GB(1)

	theAppTime.load_ItersStagesNet1DC(theConf.Iter_Stage_Net1_DC_file_pre)
	#theAppTime.print_ItersStagesNet1DC(1)
	#theAppTime.plot_ItersStagesNet1DC(1)

	theAppTime.load_ItersStagesNet2(theConf.Iter_Stage_Net2_file_pre)
	#theAppTime.print_ItersStagesNet2(1)
	#theAppTime.plot_ItersStagesNet2(1)

	theAppTime.load_ItersStagesNet2Reduce(theConf.Iter_Stage_Net2_Reduce_file_pre)
	#theAppTime.print_ItersStagesNet2Reduce(1)
	#theAppTime.plot_ItersStagesNet2Reduce(1)

	theAppTime.load_ItersCompute1(theConf.Iter_Compute1_file_pre)
	#theAppTime.print_ItersCompute1(1)
	theAppTime.load_ItersCompute2(theConf.Iter_Compute2_file_pre)
	#theAppTime.print_ItersCompute2(1)
	#theAppTime.plot_ItersCompute12_norm(1)
