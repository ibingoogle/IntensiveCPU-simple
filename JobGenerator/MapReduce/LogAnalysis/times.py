

class Time:

	time = ""

	def __init__(self,time_str):
		self.time = time_str

	def __strtolong__(self):
		return long(self.time)

	def __sub__(self,otherTime):
		return self.__strtolong__() - otherTime.__strtolong__()

	def get_second(self):
		return self.__strtolong__() / 1000.0
	
	def get_minute(self):
		return self.get_second() / 60.0

