import os
import sys
import matplotlib.pyplot as plt
from Conf import Configuration

class ExecutorSparsityBetween:

	def __init__(self):
		self.sparsity = {}
		self.sparsity['1e0f'] = []
		self.sparsity['1e-1f'] = []
		self.sparsity['1e-2f'] = []
		self.sparsity['1e-3f'] = []
		self.sparsity['1e-4f'] = []
		self.sparsity['1e-5f'] = []
		self.sparsity['1e-6f'] = []
		self.sparsity['1e-7f'] = []
		self.sparsity['1e-8f'] = []
		self.sparsity['1e-9f'] = []
		self.sparsity['1e-10f'] = []
		self.sparsity['0.0f'] = []
		return

	def add_sparsity(self, line):
		sp_line = line.split(" || ")
		if len(sp_line) != len(self.sparsity):
			print "ERROR in sparsity granularity "
			return
		self.sparsity['1e0f'].append(sp_line[0])
		self.sparsity['1e-1f'].append(sp_line[1])
		self.sparsity['1e-2f'].append(sp_line[2])
		self.sparsity['1e-3f'].append(sp_line[3])
		self.sparsity['1e-4f'].append(sp_line[4])
		self.sparsity['1e-5f'].append(sp_line[5])
		self.sparsity['1e-6f'].append(sp_line[6])
		self.sparsity['1e-7f'].append(sp_line[7])
		self.sparsity['1e-8f'].append(sp_line[8])
		self.sparsity['1e-9f'].append(sp_line[9])
		self.sparsity['1e-10f'].append(sp_line[10])
		self.sparsity['0.0f'].append(sp_line[11])
		
	def print_sparsity(self, threshold):
		print self.sparsity[threshold]
