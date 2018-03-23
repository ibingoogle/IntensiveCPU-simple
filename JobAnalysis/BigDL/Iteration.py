import os
import sys
import matplotlib.pyplot as plt

class IterTime:


	def __init__(self):
		self.list_label = ["prestages", "stage1", "stagemiddle", "stage2", "poststages"]
		self.list_time = []
		return

	def set_times(self, line):
		sp_line = line.split(" || ")
		if (len(sp_line) == 5):
			for index in range(len(self.list_label)):
				self.list_time.append(int(sp_line[index].split(" : ")[1].strip("\n")))
