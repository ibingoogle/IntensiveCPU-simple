import matplotlib.pyplot as pl
from operator import itemgetter

def draw_tasktime_host(tasktime,taskhost):
	tuple_list = []
	for i in range(0, len(tasktime)):
		tuple_list.append((tasktime[i],taskhost[i]))
	print "tuple_list: ", tuple_list
	tuple_list = sorted(tuple_list, key=itemgetter(1))
	print "tuple_list: ", tuple_list
	X = [3*x for x in range(1, len(tasktime)+1)]
	Y = []
	Z = []
	for i in range(0, len(tasktime)):
		Y.append(tuple_list[i][0])
		Z.append(tuple_list[i][1])
	print "X: ", X
	print "Y: ", Y
	print "Z: ", Z
	pl.bar(X,Y)
	pl.xticks(X,Z)
	pl.show()



def draw_tasktime(tasktime):
	X = [x for x in range(1, len(tasktime)+1)]
	Y = tasktime
	pl.bar(X,Y)
	pl.show()	
	return

def draw_tasktime_hosttime():
	return
