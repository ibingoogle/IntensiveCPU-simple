import os
import sys
import matplotlib.pyplot as plt
from Conf import Configuration

class IterStageTime:


	def __init__(self):
		self.executor_label = []
		self.dict_time_stage1 = {}
		self.dict_time_stage2 = {}
		self.list_label_stage1 = ['getweights', 'computing', 'localaggput']
		self.list_label_stage2 = ['remoteagg', 'reduceagg', 'synchronization', 'sendweights']
		return

	def add_times(self, executor, line):
		if self.dict_time_stage1.has_key(executor):
			print "ERROR, self.dict_time_stage1.has_key ", executor
			return
		self.executor_label.append(executor)
		sp_line = line.split(" || ")
		if (len(sp_line) == 7):
			time_stage1 = []
			time_stage2 = []
			for index in range(3):
				time_stage1.append(int(sp_line[index].split(" : ")[1].strip("\n")))
			for index in range(3, 7):
				time_stage2.append(int(sp_line[index].split(" : ")[1].strip("\n")))
			self.dict_time_stage2[executor] = time_stage2
			self.dict_time_stage1[executor] = time_stage1

	def print_times(self):
		print "executor_label = ", self.executor_label
		print "dict_time_stage1 = ", self.dict_time_stage1
		print "dict_time_stage2 = ", self.dict_time_stage2
