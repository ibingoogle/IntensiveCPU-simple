import os
import sys
import matplotlib.pyplot as plt
from Conf import Configuration

class IterStageNet2ReduceTime:

	def __init__(self):
		self.executor_label = []
		self.dict_time = {}
		return

	def add_times(self, executor, line):
		if self.dict_time.has_key(executor):
			print "ERROR, self.dict_time.has_key ", executor
			return
		self.executor_label.append(executor)
		time = long(line.split(" : ")[1].strip("\n"))
		self.dict_time[executor] = time

	def print_times(self):
		print "executor_label = ", self.executor_label
		print "dict_time = ", self.dict_time
