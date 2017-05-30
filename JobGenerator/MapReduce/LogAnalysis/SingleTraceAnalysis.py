import json
import numpy as np
import matplotlib.pyplot as pl
import draw as draw
from event import Event
from job import Job
from operator import itemgetter

class TraceAnalysis:
	json_path = ""

	def __init__(self,json_path_t):
		self.json_path = json_path_t
		self.job = Job()
	
	def load(self):
		try:	
			self.json_file=open(self.json_path,'r') # load .jhist file
		except IOError as error:
			print ("file open error:"+str(error))
			return 0
		return 1

	def initial_jobs(self):
		while True:
			json_str=self.json_file.readline()  # read each line in the file
			if not json_str:
				break
			elif not json_str.startswith("{"):
				continue
			else:
				json_dict = json.loads(json_str) # convert each line to dict form
				event = Event(json_dict) # pass each dict to Event class
				event.process_event(self.job) # process each dict in Event class
		return 1

	def job_startTime(self):
		return self.job.get_launchTime().__strtolong__()	

	def job_runTime(self):
		return self.job.get_runTime()

	def get_maps(self):
		return self.job.get_maps()

	def get_reduces(self):
		return self.job.get_reduces()

	def map_spendTime(self):
		times = []
		maps = self.job.get_maps()
		for maptask in maps:
			times.append(maptask.get_spendTime())
		return times

	def reduce_spendTime(self):
		times = []
		reduces = self.job.get_reduces()
		for reducetask in reduces:
			times.append(reducetask.get_spendTime())
		return times

	def map_startTime(self):
		times = []
		maps = self.job.get_maps()
		for maptask in maps:
			times.append(maptask.get_startTime().__strtolong__())
		return times

	def reduce_startTime(self):
		times = []
		reduces = self.job.get_reduces()
		for reducetask in reduces:
			times.append(reducetask.reduceattempts[0].get_startTime().__strtolong__())
		return times

	def map_finishTime(self):
		times = []
		maps = self.job.get_maps()
		for maptask in maps:
			times.append(maptask.get_finishTime().__strtolong__())
		return times

	def reduce_finishTime(self):
		times = []
		reduces = self.job.get_reduces()
		for reducetask in reduces:
			times.append(reducetask.get_finishTime().__strtolong__())
		return times

	def reduce_shuffleFinishTime(self):
		times = []
		reduces = self.job.get_reduces()
		for reducetask in reduces:
			times.append(reducetask.get_shuffleFinishTime().__strtolong__())
		return times

	def reduce_sortFinishTime(self):
		times = []
		reduces = self.job.get_reduces()
		for reducetask in reduces:
			times.append(reducetask.get_sortFinishTime().__strtolong__())
		return times

	def map_countValues(self,key):
		countValues = []
		maps = self.job.get_maps()
		for maptask in maps:
			countValues.append(maptask.get_counterValue(key))
		return countValues

	def get_mapAttemptLocality(self):
		locality = []
		maps = self.job.get_maps()
		for maptask in maps:
			locality.append(maptask.get_successAttempt().get_locality())
		return locality

	def get_mapAttemptHost(self):
		host = []
		maps = self.job.get_maps()
		for maptask in maps:
			host.append(maptask.get_successAttempt().get_hostname())
		return host

	def get_reduceAttemptHost(self):
		host = []
		reduces = self.job.get_reduces()
		for reducetask in reduces:
			host.append(reducetask.get_successAttempt().get_hostname())
		return host

	def normalrize(self,dataSet):
		normalSet = []
		tSet = []
		for i in range(0,len(dataSet)):
			tSet.append(dataSet[i])
		for i in range(0,len(dataSet)):
			normal = (float)(tSet[i])/(float)(sum(tSet))
			normalSet.append(normal)
		return normalSet


def draw_bar(plt, job_starttime, map_start_times, reduce_start_times, map_finish_times, reduce_finish_times, reduce_shuffle_finish_times, reduce_sort_finish_times, map_hosts, reduce_hosts):
	mapHosts = []
	for host in map_hosts:
		mapHosts.append(host[12:13])

	reduceHosts = []
	for host in reduce_hosts:
		reduceHosts.append(host[12:13])

	print "mapHosts: ", mapHosts
	print "reduceHosts: ", reduceHosts

	for i in range(0, len(map_start_times)):
		map_start_times[i] = map_start_times[i] - job_starttime	
	for i in range(0, len(map_finish_times)):
		map_finish_times[i] = map_finish_times[i] - job_starttime
	for i in range(0, len(reduce_start_times)):
		reduce_start_times[i] = reduce_start_times[i] - job_starttime	
	for i in range(0, len(reduce_finish_times)):
		reduce_finish_times[i] = reduce_finish_times[i] - job_starttime
	for i in range(0, len(reduce_shuffle_finish_times)):
		reduce_shuffle_finish_times[i] = reduce_shuffle_finish_times[i] - job_starttime
	for i in range(0, len(reduce_sort_finish_times)):
		reduce_sort_finish_times[i] = reduce_sort_finish_times[i] - job_starttime


	map_spend_times = []
	for i in range(0, len(map_start_times)):
		map_spend_times.append(map_finish_times[i]-map_start_times[i])
	reduce_spend_times = []
	for i in range(0, len(reduce_start_times)):
		reduce_spend_times.append(reduce_finish_times[i]-reduce_start_times[i])
	shuffle_spend_times = []
	for i in range(0, len(reduce_shuffle_finish_times)):
		shuffle_spend_times.append(reduce_shuffle_finish_times[i] - reduce_start_times[i])
	sort_spend_times = []
	for i in range(0, len(reduce_sort_finish_times)):
		sort_spend_times.append(reduce_sort_finish_times[i] - reduce_shuffle_finish_times[i])


	tuple_list = []
	for i in range(0, len(map_spend_times)):
		tuple_list.append(["m", map_spend_times[i] , map_start_times[i], mapHosts[i]])
	for i in range(0, len(reduce_spend_times)):
		tuple_list.append(["r", reduce_spend_times[i] , reduce_start_times[i], reduceHosts[i]])
	#for i in range(0, len(shuffle_spend_times)):
		#tuple_list.append(["shuffle", shuffle_spend_times[i], reduce_start_times[i], reduceHosts[i]])
	#for i in range(0, len(sort_spend_times)):
		#tuple_list.append(["sort", sort_spend_times[i], reduce_shuffle_finish_times[i], reduceHosts[i]])

	tuple_list = sorted(tuple_list, key = itemgetter(3,2))
	print "tuple_list: ", tuple_list
	
	X = []
	X_replace = []
	for i in range(0, len(tuple_list)):
		X.append(2*(i+1)-1)
		X_replace.append(tuple_list[i][3])

	map_width = 0.8
	reduce_width = 0.8
	for i in range(0, len(tuple_list)):
		if tuple_list[i][0] == "m":
			plt.bar(2*(i+1)-1, tuple_list[i][1], map_width, bottom = tuple_list[i][2])
		if tuple_list[i][0] == "r":
			plt.bar(2*(i+1)-1, tuple_list[i][1], reduce_width, bottom = tuple_list[i][2], color='r')
		#if tuple_list[i][0] == "shuffle":
			#plt.bar(2*(i+1)-1, tuple_list[i][1], reduce_width, bottom = tuple_list[i][2], color='g')
		#if tuple_list[i][0] == "sort":
			#plt.bar(2*(i+1)-1, tuple_list[i][1], reduce_width, bottom = tuple_list[i][2], color='k')

	
	plt.xticks(X,X_replace)
	plt.show()
"""
#	for i in range(0, len(map_start_times)):
		map_start_times[i] = map_start_times[i] - job_starttime	
	for i in range(0, len(map_finish_times)):
		map_finish_times[i] = map_finish_times[i] - job_starttime
	for i in range(0, len(reduce_shuffle_finish_times)):
		reduce_shuffle_finish_times[i] = reduce_shuffle_finish_times[i] - job_starttime

	print "map size in jobs: ", len(map_start_times)

	L = range(1, len(map_start_times)+1)
	H = []
	for i in range(0, len(map_finish_times)):
		H.append(map_finish_times[i] - map_start_times[i])

	tuple_list = []
	for i in range(0, len(mapHosts)):
		tuple_list.append((map_start_times[i], H[i], mapHosts[i]))
	tuple_list = sorted(tuple_list, key = itemgetter(2))

	print "L: ", L
	print "H: ", H
	print "tuple_list: ", tuple_list

	W = 0.7
	B = map_start_times
	X = []
	Z = []
	shuffle_start = len(map_start_times) - len(reduce_shuffle_finish_times)
	print "shuffle_start: ", shuffle_start
	print "B: ", B

	for i in range(0, len(map_start_times)):
		X.append(2*L[i] - 1)
		Z.append(tuple_list[i][2])
		print "i: ", i
		print "tuple_list[i][1]: ", tuple_list[i][1]
		print "tuple_list[i][0]: ", tuple_list[i][0]
		plt.bar(2*L[i] - 1, tuple_list[i][1], W, bottom = tuple_list[i][0])
	
	for i in range(shuffle_start, len(map_start_times)):
		print "i: ", i
		print "reduce_shuffle_finish_times[i-shuffle_start]-B[i]: ", reduce_shuffle_finish_times[i-shuffle_start]-B[i]
		print "B[i]: ", B[i]
		plt.bar(2*L[i]-1, reduce_shuffle_finish_times[i-shuffle_start]-B[i], W-0.5, bottom=B[i], color='r' )

	print Z
	plt.xticks(X,Z)
	plt.show()

"""


if __name__ == "__main__":
	TraceAnalyzer = TraceAnalysis("./jobs/jobs1.jhist")
	if TraceAnalyzer.load() == 0:
		print "load error"
	if TraceAnalyzer.initial_jobs() == 0:
		print "initial job error"
	

	job_startTime = TraceAnalyzer.job_startTime()
	print "job_startTime:", job_startTime


	reduce_start_times = []
	reduce_start_times.extend(TraceAnalyzer.reduce_startTime())

	reduce_finish_times = []
	reduce_finish_times.extend(TraceAnalyzer.reduce_finishTime())
	
	reduce_hosts = []
	reduce_hosts.extend(TraceAnalyzer.get_reduceAttemptHost())

	map_start_times = []
	map_start_times.extend(TraceAnalyzer.map_startTime())

	map_finish_times = []
	map_finish_times.extend(TraceAnalyzer.map_finishTime())

	map_hosts = []
	map_hosts.extend(TraceAnalyzer.get_mapAttemptHost())

	reduce_shuffle_finish_times = []
	reduce_shuffle_finish_times.extend(TraceAnalyzer.reduce_shuffleFinishTime())

	reduce_sort_finish_times = []
	reduce_sort_finish_times.extend(TraceAnalyzer.reduce_sortFinishTime())
	
	print "map_start_times: ", map_start_times
	#pl.figure(4)  # create figure 4
	#draw.draw_tasktime_host(map_locality_data,mapAttemptHosts)

	#pl.figure(5)
	draw_bar(pl, job_startTime, map_start_times, reduce_start_times, map_finish_times, reduce_finish_times, reduce_shuffle_finish_times, reduce_sort_finish_times, map_hosts,reduce_hosts)
	
