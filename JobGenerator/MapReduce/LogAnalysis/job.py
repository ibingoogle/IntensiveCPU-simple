from map import Map
from reduce import Reduce
from times import Time

class Job:

	job = {}
	maps = []	# list all maps
	reduces = []	# list all reduces	

	def __init__(self):
		self.maps = []
		self.reduces = []
		self.job = {}
		return

    	def process_jobEvent(self,eventType,eventValue):
		if eventType == "JOB_SUBMITTED":
			print "job_submitted"
			self.job["jobid"]    = eventValue["jobid"]
			self.job["userName"] = eventValue["userName"]
			self.job["jobName"]  = eventValue["jobName"]
			self.job["submitTime"] = eventValue["submitTime"]
		elif eventType == "JOB_INITED":
			print "job_inited"
			self.job["launchTime"] = eventValue["launchTime"]
			self.job["totalMaps"]  = eventValue["totalMaps"]
			self.job["toalReduces"]= eventValue["totalReduces"]
		elif eventType == "JOB_FINISHED":
			print "job_finished"
			self.job["finishTime"]   = eventValue["finishTime"]
			self.job["failedMaps"]   = eventValue["failedMaps"]
			self.job["failedReduces"]= eventValue["failedReduces"]

	def process_tasksEvent(self,eventType,eventValue):
		if eventType.startswith("TASK"):
			print "tasksEvent"
			if eventValue["taskType"] == "MAP":
				if eventType == "TASK_STARTED": # pass info to map class
					nmap = Map()
					nmap.process_taskEvent(eventType,eventValue) # pass info to new created map class and add it to self.maps
					self.maps.append(nmap)
				else: #pass info to old map class
					self.get_map(eventValue["taskid"]).process_taskEvent(eventType,eventValue)
			elif eventValue["taskType"] == "REDUCE":
				if eventType == "TASK_STARTED": # pass info to reduce class
					nreduce = Reduce()
					nreduce.process_taskEvent(eventType,eventValue) # pass info to new created reduce class and add it to self.reduces
					self.reduces.append(nreduce)
				else: #pass info to old reduce class
					self.get_reduce(eventValue["taskid"]).process_taskEvent(eventType,eventValue)
		elif eventType.startswith("MAP_ATTEMPT"): #pass info to mapattempt in old map class
			print "map_attempt"
			self.get_map(eventValue["taskid"]).process_taskEvent(eventType,eventValue)
		elif eventType.startswith("REDUCE_ATTEMPT"): #pass info to reduceattempt in old reduce class
			print "reduce_attempt"
			self.get_reduce(eventValue["taskid"]).process_taskEvent(eventType,eventValue)


	def get_map(self,mapid):
		for maptask in self.maps:
			if maptask.get_taskid() == mapid:
				return maptask
		return

	def get_reduce(self,reduceid):
		for reducetask in self.reduces:
			if reducetask.get_taskid() == reduceid:
				return reducetask
		return

	def get_maps(self):
		tasks = []
		for task in self.maps:
			if task.status == "SUCCEEDED":
				tasks.append(task)
		return tasks

	def get_reduces(self):
		tasks = []
		for task in self.reduces:
			if task.status == "SUCCEEDED":
				tasks.append(task)
		return tasks

	def get_launchTime(self):
		time = Time(self.job["launchTime"])
		return time

	def get_finishTime(self):
		time = Time(self.job["finishTime"])
		return time

	def get_runTime(self):
		if self.get_finishTime().__strtolong__() <=0:
			return 0
		elif self.get_launchTime().__strtolong__() <=0:
			return 0
		else:
			return self.get_finishTime().__sub__(self.get_launchTime())
