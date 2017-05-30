import json
import numpy as np
import matplotlib.pyplot as pl
import draw as draw
from event import Event
from job import Job
from operator import itemgetter
import os

#5m_10queue*5

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
				self.event = Event(json_dict) # pass each dict to Event class
				self.event.process_event(self.job) # process each dict in Event class
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


def draw_bar(plt, job_number, job_starttime, map_start_times, reduce_start_times, map_finish_times, reduce_finish_times, reduce_shuffle_finish_times, reduce_sort_finish_times, map_hosts, reduce_hosts):

	mapHosts = []
	reduceHosts = []
	for i in range(0, job_number):
		hosts_map = []	
		for host in map_hosts[i]:
			hosts_map.append(host[12:13])
		mapHosts.append(hosts_map)
		hosts_reduce = []
		for host in reduce_hosts[i]:
			hosts_reduce.append(host[12:13])
		reduceHosts.append(hosts_reduce)
	print "mapHosts: ", mapHosts
	print "reduceHosts: ", reduceHosts

	for i in range(0, job_number):
		for j in range(0, len(map_start_times[i])):
			map_start_times[i][j] = map_start_times[i][j] - job_starttime	
		for j in range(0, len(map_finish_times[i])):
			map_finish_times[i][j] = map_finish_times[i][j] - job_starttime
		for j in range(0, len(reduce_start_times[i])):
			reduce_start_times[i][j] = reduce_start_times[i][j] - job_starttime	
		for j in range(0, len(reduce_finish_times[i])):
			reduce_finish_times[i][j] = reduce_finish_times[i][j] - job_starttime
		for j in range(0, len(reduce_shuffle_finish_times[i])):
			reduce_shuffle_finish_times[i][j] = reduce_shuffle_finish_times[i][j] - job_starttime
		for j in range(0, len(reduce_sort_finish_times[i])):
			reduce_sort_finish_times[i][j] = reduce_sort_finish_times[i][j] - job_starttime
	print "map_start_times: ", map_start_times
	print "map_finish_times: ", map_finish_times
	print "reduce_start_times: ", reduce_start_times
	print "reduce_finish_times: ", reduce_finish_times
	print "reduce_shuffle_finish_times: ", reduce_shuffle_finish_times
	print "reduce_sort_finish_times: ", reduce_sort_finish_times


	map_spend_times = []
	reduce_spend_times = []
	shuffle_spend_times = []
	sort_spend_times = []
	for i in range(0, job_number):
		map_spend_times_each = []
		reduce_spend_times_each = []
		shuffle_spend_times_each = []
		sort_spend_times_each = []
		for j in range(0, len(map_start_times[i])):
			map_spend_times_each.append(map_finish_times[i][j]-map_start_times[i][j])
		for j in range(0, len(reduce_start_times[i])):
			reduce_spend_times_each.append(reduce_finish_times[i][j]-reduce_start_times[i][j])
		for j in range(0, len(reduce_shuffle_finish_times[i])):
			shuffle_spend_times_each.append(reduce_shuffle_finish_times[i][j] - reduce_start_times[i][j])	
		for j in range(0, len(reduce_sort_finish_times[i])):
			sort_spend_times_each.append(reduce_sort_finish_times[i][j] - reduce_shuffle_finish_times[i][j])
		map_spend_times.append(map_spend_times_each)
		reduce_spend_times.append(reduce_spend_times_each)
		shuffle_spend_times.append(shuffle_spend_times_each)
		sort_spend_times.append(sort_spend_times_each)
	print "map_spend_times: ", map_spend_times
	print "reduce_spend_times: ", reduce_spend_times
	print "shuffle_spend_times: ", shuffle_spend_times
	print "sort_spend_times: ", sort_spend_times
	

	colors = ['b','y','r','k','m','c','g']		
	for i in range(0, job_number):
		tuple_list = []
		for j in range(0, len(map_spend_times[i])): #add map tasks into tuple_list
			tuple_list.append(["m", map_spend_times[i][j] , map_start_times[i][j], mapHosts[i][j]])
		for j in range(0, len(reduce_spend_times[i])): #add reduce tasks into tuple_list
			tuple_list.append(["r", reduce_spend_times[i][j] , reduce_start_times[i][j], reduceHosts[i][j]])
		tuple_list = sorted(tuple_list, key = itemgetter(3,2))  #sort based on hosts first, then on start_time
		X = []
		X_replace = []
		for j in range(0, len(tuple_list)): # replace the index with hosts number
			X.append(2*(j+1)-1)
			X_replace.append(tuple_list[j][3]) 
		map_width = 0.8  # the width of the bar
		reduce_width = 0.8
		#for j in range(0, len(tuple_list)):
			#if tuple_list[j][0] == "m":
				#plt.bar(2*(j+1)-1, tuple_list[j][1], map_width, bottom = tuple_list[j][2])
			#if tuple_list[j][0] == "r":
				#plt.bar(2*(j+1)-1, tuple_list[j][1], reduce_width, bottom = tuple_list[j][2], color='r')
		#plt.xticks(X,X_replace)
		#plt.show()



	all_tuple_list = []
	for i in range(0, job_number):# add all tasks 
		for j in range(0, len(map_spend_times[i])): # add all map tasks into all_tuple_list, i indicates to which job the task belong 
			all_tuple_list.append(["m", map_spend_times[i][j], map_start_times[i][j], mapHosts[i][j], i%len(colors)])
		for j in range(0, len(reduce_spend_times[i])): # add all reduce tasks into all_tuple_list
			all_tuple_list.append(["r", reduce_spend_times[i][j], reduce_start_times[i][j], reduceHosts[i][j], i%len(colors)])
			all_tuple_list.append(["s", shuffle_spend_times[i][j], reduce_start_times[i][j], reduceHosts[i][j], i%len(colors)])
	all_tuple_list = sorted(all_tuple_list, key = itemgetter(3,2)) # sort based on hosts and start_times
	
	X = []
	X_replace = []
	# index replacement
	for i in range(0, len(all_tuple_list)):
		X.append(2*(i+1)-1)
		X_replace.append(all_tuple_list[i][3])
	
	map_width = 0.8
	reduce_width = 0.8
	
	for i in range(0, job_number):
		print "The following is the colors representing job number ", i
		print "The map task color is ", colors[i%len(colors)]
		print "The reduce task color is ", colors[i%len(colors)]
	
	for i in range(0, len(all_tuple_list)):
		if all_tuple_list[i][0] == "m":
			print "all_tuple_list[i][4]*2: ", all_tuple_list[i][4]
			print "colors[all_tuple_list[i][4]*2]: ", colors[all_tuple_list[i][4]]
			plt.bar(2*(i+1)-1, all_tuple_list[i][1], map_width, bottom = all_tuple_list[i][2], color = colors[all_tuple_list[i][4]]) # i decides the bar's color
		if all_tuple_list[i][0] == "r":
			print "all_tuple_list[i][4]*2: ", all_tuple_list[i][4]
			print "colors[all_tuple_list[i][4]*2]: ", colors[all_tuple_list[i][4]]
			plt.bar(2*(i+1)-1, all_tuple_list[i][1], reduce_width, bottom = all_tuple_list[i][2], color = colors[all_tuple_list[i][4]])
		if all_tuple_list[i][0] == "s":
			plt.bar(2*(i+1)-1, all_tuple_list[i][1], reduce_width, bottom = all_tuple_list[i][2], color = "g")
	plt.xticks(X,X_replace)
	plt.show()


def statistics(job_number, map_hosts, reduce_hosts):
	mapHosts = []
	reduceHosts = []
	for i in range(0, job_number):
		hosts_map = []	
		for host in map_hosts[i]:
			hosts_map.append(host[12:13])
		mapHosts.append(hosts_map)
		hosts_reduce = []
		for host in reduce_hosts[i]:
			hosts_reduce.append(host[12:13])
		reduceHosts.append(hosts_reduce)
	print "mapHosts: ", mapHosts
	print "reduceHosts: ", reduceHosts

	mapNumber = []
	for i in range(0,job_number):
		number = len(mapHosts[i])
		mapNumber.append(number)
	print "mapNumber: ", mapNumber

	hostMaps = []
	hostReduces = []
	for i in range(0,job_number):
		hosts = [0,0,0,0,0]
		for host in mapHosts[i]:
			hosts[int(host)-1] += 1
		hostMaps.append(hosts)
		print "hostMaps: ", hosts
		hosts = [0,0,0,0,0]
		for host in reduceHosts[i]:
			hosts[int(host)-1] += 1
		hostReduces.append(hosts)
		print "hostReduces: ", hosts
		
		
	for i in range(0,job_number):
		print "In job ", i
		reduce_count = 0
		host_count = 0
		for host in hostReduces[i]:
			host_count += 1
			for j in range(0, int(host)):
				reduce_count += 1
				locality = float(hostMaps[i][host_count-1])/float(mapNumber[i])
				print "Locality in reduce task ", reduce_count, " is ", locality, ": ", hostMaps[i][host_count-1], " out of ", mapNumber[i]


if __name__ == "__main__":
	TraceAnalyzer = []

	path = "./jobs/";
	filelist = os.listdir(path)
	for file in filelist:
		filedir = os.path.join(path,file)
		if os.path.isdir(filedir):
			continue
		TraceAnalyzer.append(TraceAnalysis(filedir))

	for i in range(0, len(TraceAnalyzer)):
		print i
		if TraceAnalyzer[i].load() == 0:
			print "load error"
		if TraceAnalyzer[i].initial_jobs() == 0:
			print "initial job error"

	for i in range(0, len(TraceAnalyzer)):
		print "TraceAnalyzer[i].job.job: ", TraceAnalyzer[i].job.job
		
	job_startTime = TraceAnalyzer[0].job_startTime()
	for i in range(1, len(TraceAnalyzer)):
		if TraceAnalyzer[i].job_startTime() < job_startTime:
			job_startTime = TraceAnalyzer[i].job_startTime()

	print "job_startTime: ", job_startTime

	reduce_start_times = []
	reduce_finish_times = []
	reduce_shuffle_finish_times = []
	reduce_sort_finish_times = []
	reduce_hosts = []
	map_start_times = []
	map_finish_times = []
	map_hosts = []
	for i in range(0, len(TraceAnalyzer)):
		reduce_start_times.append(TraceAnalyzer[i].reduce_startTime())
		reduce_finish_times.append(TraceAnalyzer[i].reduce_finishTime())
		reduce_hosts.append(TraceAnalyzer[i].get_reduceAttemptHost())
		reduce_shuffle_finish_times.append(TraceAnalyzer[i].reduce_shuffleFinishTime())
		reduce_sort_finish_times.append(TraceAnalyzer[i].reduce_sortFinishTime())
		map_start_times.append(TraceAnalyzer[i].map_startTime())
		map_finish_times.append(TraceAnalyzer[i].map_finishTime())
		map_hosts.append(TraceAnalyzer[i].get_mapAttemptHost())
	print "map_start_times: ", map_start_times
	print "map_finish_times: ", map_finish_times
	print "map_hosts: ", map_hosts
	print "reduce_start_times: ", reduce_start_times
	print "reduce_finish_times: ", reduce_finish_times
	print "reduce_shuffle_finish_times: ", reduce_shuffle_finish_times
	print "reduce_sort_finish_times: ", reduce_sort_finish_times
	print "reduce_hosts: ", reduce_hosts

	statistics(len(TraceAnalyzer), map_hosts, reduce_hosts)
	
	draw_bar(pl, len(TraceAnalyzer), job_startTime, map_start_times, reduce_start_times, map_finish_times, reduce_finish_times, reduce_shuffle_finish_times, reduce_sort_finish_times, map_hosts,reduce_hosts)
