#!/bin/python
import subprocess
import os
import sys

pid_file=sys.path[0]

try:
    file = open(pid_file + "/NetworkMonitor_pid", "r")
    pid = file.readline()
except (IOError,OSError) as error:
    print("error during cluster_file loading %s", error)
print(pid)
command = "kill -s 9 " + str(pid)
val = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
val.wait()

