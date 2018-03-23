import os
import sys
import matplotlib.pyplot as plt
from Conf import Configuration

class IterCompute1Time:

	def __init__(self):
		self.executor_label = []
		self.dict_time_forward = {}
		self.dict_time_forward_norm = {}
		return

	def add_times(self, executor, line):
		if self.dict_time_forward.has_key(executor):
			print "ERROR, self.dict_time_forward.has_key ", executor
			return
		self.executor_label.append(executor)
		sp_line = line.split(" , ")
		time_forward = []
		for index in range(len(sp_line)-1):
			time_forward.append(int(sp_line[index]))
		self.dict_time_forward[executor] = time_forward

	def norm_times(self, executor):
		time_forward = self.dict_time_forward[executor]
		maxtime = float(time_forward[len(time_forward)-1])
		time_forward_norm = []
		for index in range(len(time_forward)):
			time_forward_norm.append(float(time_forward[index])/maxtime + 0.1)
		self.dict_time_forward_norm[executor] = time_forward_norm

	def print_times(self):
		print "executor_label = ", self.executor_label
		print "dict_time_forward = ", self.dict_time_forward
		print "dict_time_forward_norm", self.dict_time_forward_norm
