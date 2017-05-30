
class Event:

	event={}

	def __init__(self,event_dict):
		self.event = event_dict
	
	def get_eventType(self):
		return self.event["type"]

	def get_eventValue(self):
		return self.event["event"].values()[0]

	def process_event(self,job):	#process each dick according to starts
		if self.get_eventType().startswith("JOB"):	# extract job info
			job.process_jobEvent(self.get_eventType(),self.get_eventValue())
		elif self.get_eventType().startswith("TASK") or self.get_eventType().startswith("MAP_ATTEMPT") or self.get_eventType().startswith("REDUCE_ATTEMPT"):	# extrect tasks info
			job.process_tasksEvent(self.get_eventType(),self.get_eventValue())









