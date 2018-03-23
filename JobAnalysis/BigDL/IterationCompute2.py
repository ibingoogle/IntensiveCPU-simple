import os
import sys
import matplotlib.pyplot as plt
from Conf import Configuration

class IterCompute2Time:

	def __init__(self):
		self.executor_label = []
		self.dict_time_backward = {}
		self.dict_time_backward_norm = {}
		return

	def add_times(self, executor, line):
		if self.dict_time_backward.has_key(executor):
			print "ERROR, self.dict_time_backward.has_key ", executor
			return
		self.executor_label.append(executor)
		sp_line = line.split(" , ")
		time_backward = []
		for index in range(len(sp_line)-1):
			time_backward.append(int(sp_line[index]))
		self.dict_time_backward[executor] = time_backward

	def norm_times(self, executor):
		time_backward = self.dict_time_backward[executor]
		maxtime = float(time_backward[len(time_backward)-1])
		time_backward_norm = []
		for index in range(len(time_backward)):
			time_backward_norm.append(float(time_backward[index])/maxtime + 0.1)
		self.dict_time_backward_norm[executor] = time_backward_norm

	def print_times(self):
		print "executor_label = ", self.executor_label
		print "dict_time_backward = ", self.dict_time_backward
		print "dict_time_backward_norm", self.dict_time_backward_norm
