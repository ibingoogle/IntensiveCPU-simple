import os
import sys
import matplotlib.pyplot as plt
from Conf import Configuration

class IterStageNet1DCTime:

	def __init__(self):
		self.executor_label = []
		self.dict_time = {}
		self.dict_block_label = {}
		return

	def add_times(self, executor, line):
		if self.dict_time.has_key(executor):
			print "ERROR, self.dict_time.has_key ", executor
			return
		#print executor
		self.executor_label.append(executor)
		block_label = []
		time = {}
		sp_line = line.split(" || ")
		for index in range(len(sp_line)-1):
			sub_line = sp_line[index]
			#print sub_line
			sp_sub_line = sub_line.split(" : ")
			block_label.append(sp_sub_line[0])
			time_start_end = []
			time_start_end.append(long(sp_sub_line[1].strip("\n")))
			time_start_end.append(long(sp_sub_line[2].strip("\n")))
			time[sp_sub_line[0]] = time_start_end
		self.dict_time[executor] = time
		self.dict_block_label[executor] = block_label

	def norm_times(self, executor):
		starttime = 0L
		time = self.dict_time[executor]
		for blockId in self.dict_block_label[executor]:
			time_start_end = time[blockId]
			if starttime == 0L:
				starttime = time_start_end[0]
			elif starttime > time_start_end[0]:
				starttime = time_start_end[0]
		for blockId in self.dict_block_label[executor]:
			time_start_end = time[blockId]
			time_start_end[0] = time_start_end[0] - starttime
			time_start_end[1] = time_start_end[1] - starttime
		#print starttime

	def print_times(self):
		print "executor_label = ", self.executor_label
		print "dict_time = ", self.dict_time
		print "dict_block_label = ", self.dict_block_label
