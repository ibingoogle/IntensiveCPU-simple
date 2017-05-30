from times import Time
from counter import Counter

class Reduce:

	status = ""
	reducetask = {}	# contain info about reduce task
	reduceattempts = [] # list each reduce attempt

	def __init__(self):
		self.reducetask = {}
		self.reduceattempts = []
		self.counter = Counter()
		self.register_counter()
		return

	def register_counter(self):
		self.counter.register_property("FILE_BYTES_READ")
		self.counter.register_property("FILE_BYTES_WRITTEN")
		self.counter.register_property("HDFS_BYTES_READ")
		self.counter.register_property("HDFS_BYTES_WRITTEN")
		self.counter.register_property("COMBINE_INPUT_RECORDS")
		self.counter.register_property("COMBINE_OUTPUT_RECORDS")
		self.counter.register_property("REDUCE_INPUT_GROUPS")
		self.counter.register_property("REDUCE_SHUFFLE_BYTES")
		self.counter.register_property("REDUCE_INPUT_RECORDS");
		self.counter.register_property("REDUCE_OUTPUT_RECORDS");
		self.counter.register_property("SPILLED_RECORDS")
		self.counter.register_property("SHUFFLED_MAPS");
		self.counter.register_property("FAILED_SHUFFLE");
		self.counter.register_property("MERGED_MAP_OUTPUTS");
		self.counter.register_property("CPU_MILLISECONDS")
		self.counter.register_property("PHYSICAL_MEMORY_BYTES")
		self.counter.register_property("VIRTUAL_MEMORY_BYTES")
		self.counter.register_property("COMMITTED_HEAP_BYTES")
		self.counter.register_property("GC_TIME_MILLIS")


	def process_taskEvent(self,eventType,eventValue):
		if eventType == "TASK_STARTED":
			print "task_started of reduce"
			self.reducetask["taskid"] = eventValue["taskid"]
			self.reducetask["startTime"] = eventValue["startTime"]
			self.reducetask["splitLocations"] = eventValue["splitLocations"]
		elif eventType == "TASK_FINISHED":
			print "task_finished of reduce"
			self.reducetask["finishTime"] = eventValue["finishTime"]
			self.reducetask["successfulAttemptId"] = eventValue["successfulAttemptId"]
			for groupList in eventValue["counters"]["groups"]:
				self.process_counterValue(groupList["counts"])
                        self.status = "SUCCEEDED"
                elif eventType == "TASK_FAILED" or eventType == "TASK_KILLED":
			print "task_failed of reduce"
			self.reducetask["finishTime"] = eventValue["finishTime"] 
                        self.status = "FAILED"
		elif eventType.startswith("REDUCE_ATTEMPT"):
			if eventType == "REDUCE_ATTEMPT_STARTED":
				reduceattempt=ReduceAttempt() # pass info to new created reduceattempt class and add it to self.reduceattempts
				reduceattempt.process_taskAttemptEvent(eventType,eventValue)
				self.reduceattempts.append(reduceattempt)
			else:
				self.get_attempt(eventValue["attemptId"]).process_taskAttemptEvent(eventType,eventValue)

	def process_counterValue(self,counterList):
		for counterValue in counterList:
			self.counter.add_property(counterValue["name"],counterValue["value"])


	def get_attempt(self,attemptid):
		for attempt in self.reduceattempts:
			if attempt.get_attemptid()==attemptid:
				return attempt
		return

	def get_successAttempt(self):
		for attempt in self.reduceattempts:
			if attempt.get_attemptStatus() == "SUCCEEDED":
				return attempt	

	def get_taskid(self):
		return self.reducetask["taskid"]

	def get_attmptTimes(self):
		return len(self.reduceattempts)

	def get_startTime(self):
		attempt = self.get_successAttempt()
		time = attempt.get_startTime()
		return time

	def get_taskstartTime(self):
		return self.reducetask["startTime"]

	def get_finishTime(self):
		attempt = self.get_successAttempt()
		time = attempt.get_finishTime()
		return time

	def get_taskfinishTime(self):
		return self.reducetask["finishTime"]

	def get_shuffleFinishTime(self):
		attempt = self.get_successAttempt()
		time = attempt.get_shuffleFinishTime()
		return time

	def get_sortFinishTime(self):
		attempt = self.get_successAttempt()
		time = attempt.get_sortFinishTime()
		return time

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
	


class ReduceAttempt:

	status=""
	reduceattempt = {}
		
	def __init__(self):
		self.reduceattempt = {}
		return
	
	def process_taskAttemptEvent(self,eventType,eventValue):
		if eventType == "REDUCE_ATTEMPT_STARTED":
			print "reduce_attempt: started"
			self.reduceattempt["attemptId"] = eventValue["attemptId"]
			self.reduceattempt["startTime"]=eventValue["startTime"]
			self.reduceattempt["containerId"] = eventValue["containerId"]
			self.reduceattempt["locality"] = eventValue["locality"]["string"]
			print self.reduceattempt["locality"]
		elif eventType == "REDUCE_ATTEMPT_FINISHED":
			print "reduce_attempt: finished"
			self.reduceattempt["hostname"] = eventValue["hostname"]
			self.reduceattempt["finishTime"] = eventValue["finishTime"]
			self.reduceattempt["taskStatus"] = eventValue["taskStatus"]
			self.reduceattempt["shuffleFinishTime"] = eventValue["shuffleFinishTime"]
			self.reduceattempt["sortFinishTime"] = eventValue["sortFinishTime"]
			self.status = "SUCCEEDED"
			print self.reduceattempt["hostname"]
		else:
			print "reduce_attempt: failed"
			self.status = "FAILED"

	def get_attemptid(self):
		return self.reduceattempt["attemptId"]

	def get_startTime(self):
		return Time(self.reduceattempt["startTime"])

	def get_shuffleFinishTime(self):
		return Time(self.reduceattempt["shuffleFinishTime"])

	def get_sortFinishTime(self):
		return Time(self.reduceattempt["sortFinishTime"])

	def get_finishTime(self):
		return Time(self.reduceattempt["finishTime"])

	def get_hostname(self):
		return self.reduceattempt["hostname"]

	def get_locality(self):
		return self.reduceattempt["locality"]
	
	def get_attemptStatus(self):
		return self.status		
			
