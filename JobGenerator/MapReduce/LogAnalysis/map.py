from counter import Counter
from times import Time


class Map:

	status = ""
	maptask = {}	# contain info about map task
	mapattempts = [] # list each map attempt

	def __init__(self):
		self.maptask = {}
		self.mapattempts = []
		self.counter = Counter()
		self.register_counter()
		return

	def register_counter(self):
		self.counter.register_property("FILE_BYTES_READ")
		self.counter.register_property("FILE_BYTES_WRITTEN")
		self.counter.register_property("HDFS_BYTES_READ")
		self.counter.register_property("HDFS_BYTES_WRITTEN")
		self.counter.register_property("MAP_INPUT_RECORDS")
		self.counter.register_property("MAP_OUTPUT_RECORDS")
		self.counter.register_property("SPLIT_RAW_BYTES")
		self.counter.register_property("COMBINE_INPUT_RECORDS")
		self.counter.register_property("COMBINE_OUTPUT_RECORDS")
		self.counter.register_property("SPILLED_RECORDS")
		self.counter.register_property("CPU_MILLISECONDS")
		self.counter.register_property("PHYSICAL_MEMORY_BYTES")
		self.counter.register_property("VIRTUAL_MEMORY_BYTES")
		self.counter.register_property("COMMITTED_HEAP_BYTES")
		self.counter.register_property("GC_TIME_MILLIS")
		self.counter.register_property("MERGED_MAP_OUTPUTS")


	def process_taskEvent(self,eventType,eventValue):
		if eventType == "TASK_STARTED":
			print "task_started of map"
			self.maptask["taskid"] = eventValue["taskid"]
			self.maptask["startTime"] = eventValue["startTime"]
			self.maptask["splitLocations"] = eventValue["splitLocations"]
		elif eventType == "TASK_FINISHED":
			print "task_finished of map"
			self.maptask["finishTime"] = eventValue["finishTime"]
			self.maptask["successfulAttemptId"] = eventValue["successfulAttemptId"]
                        self.status = "SUCCEEDED"
			for groupList in eventValue["counters"]["groups"]:
				self.process_counterValue(groupList["counts"])
                elif eventType == "TASK_FAILED" or eventType == "TASK_KILLED":
			print "task_failed of map"
			self.maptask["finishTime"] = eventValue["finishTime"] 
                        self.status = "FAILED"
		elif eventType.startswith("MAP_ATTEMPT"):
			#print "MMMMMMMMMMMMMMMMMMMMMMMMMMAP_ATTEMPT"
			if eventType == "MAP_ATTEMPT_STARTED":
				#print "MMMMMMMMMMMMMMMMMMMMMMMMMMMAP_ATTEMPT_STARTED"
				nmapattempt = MapAttempt()  # pass info to new created mapattempt class and add it to self.mapattempts
				nmapattempt.process_taskAttemptEvent(eventType,eventValue)
				self.mapattempts.append(nmapattempt)
			else:
				#print eventType
				#print eventValue
				if self.get_attempt(eventValue["attemptId"]) != None:
					self.get_attempt(eventValue["attemptId"]).process_taskAttemptEvent(eventType,eventValue)


	def process_counterValue(self,counterList):
		for counterValue in counterList:
			self.counter.add_property(counterValue["name"],counterValue["value"])

	def get_counterValue(self,key):
		return self.counter.get_value(key)

	def get_attempt(self,attemptid):
		for attempt in self.mapattempts:
			if attempt.get_attemptid() == attemptid:
				return attempt
		return

	def get_successAttempt(self):
		for attempt in self.mapattempts:
			if attempt.get_attemptStatus() == "SUCCEEDED":
				return attempt

	def get_splitLocations(self):
		return self.maptask["splitLocations"]

	def get_taskid(self):
		return self.maptask["taskid"]

	def get_attmptTimes(self):
		return len(self.mapattempts)

	def get_startTime(self):
		attempt = self.get_successAttempt()
		time = attempt.get_startTime()
		return time

	def get_taskstartTime(self):
		return self.maptask["startTime"]

	def get_finishTime(self):
		attempt = self.get_successAttempt()
		time = attempt.get_finishTime()
		return time

	def get_taskfinishTime(self):
		return self.maptask["finishTime"]


	def get_spendTime(self):
		if self.get_finishTime().__strtolong__() < 0:
			return 0
		elif self.get_startTime().__strtolong__() < 0:
			return 0
		else:
			return self.get_finishTime().__sub__(self.get_startTime())

	def get_taskspendTime(self):
		if self.get_taskfinishTime().__strtolong__() < 0:
			return 0
		elif self.get_taskstartTime().__strtolong__() < 0:
			return 0
		else:
			return self.get_taskfinishTime().__sub__(self.get_taskstartTime())

class MapAttempt:

	status=""

	mapattempt = {}

	def __init__(self):
		self.mapattempt = {}
		return

	def process_taskAttemptEvent(self,eventType,eventValue):
		#print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		if eventType == "MAP_ATTEMPT_STARTED":
			print "map_attempt:started"
			self.mapattempt["attemptId"]=eventValue["attemptId"]
			self.mapattempt["startTime"]=eventValue["startTime"]
			self.mapattempt["containerId"] = eventValue["containerId"]
			self.mapattempt["locality"] = eventValue["locality"]["string"]
			print self.mapattempt["locality"]
		elif eventType == "MAP_ATTEMPT_FINISHED":
			print "map_attempt:finished"
			self.status = "SUCCEEDED"
			self.mapattempt["finishTime"] = eventValue["finishTime"]
			self.mapattempt["mapfinishTime"] = eventValue["mapFinishTime"]
			self.mapattempt["taskStatus"] = eventValue["taskStatus"]
			self.mapattempt["hostname"]   = eventValue["hostname"]
			print self.mapattempt["hostname"]
		elif eventType == "MAP_ATTEMPT_KILLED":
			#print eventValue
			#print eventType
			self.status = "FAILED"
		else:
			#print eventValue
			#print eventType
			self.status = "FAILED"
			

	def get_attemptid(self):
		return self.mapattempt["attemptId"]

	def get_attemptStatus(self):
		return self.status

	def get_hostname(self):
		return self.mapattempt["hostname"]

	def get_startTime(self):
		time = Time(self.mapattempt["startTime"])
		return time

	def get_finishTime(self):
		time = Time(self.mapattempt["finishTime"])
		return time
	
	def get_locality(self):
		return self.mapattempt["locality"]
		
	def get_containerId(self):
		return self.mapattempt["containerId"]

	def get_spendTime(self):
		if self.get_finishTime().__strtolong__() <= 0:
			return 0
		elif self.get_startTime().__strtolong__() <= 0:
			return 0
		else:
			return self.get_finishTime().__sub__(self.get_startTime())
